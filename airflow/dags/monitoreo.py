from airflow import DAG
from airflow.operators.python import PythonOperator
import numpy as np
import pandas as pd
from databank_mlops.app.schemas.predict import PredictRequest
from databank_mlops.components.transformation.preprocessors.field_text_to_number import (
    mb_clean_text_number,
)
from databank_mlops.components.transformation.preprocessors.field_text import (
    mb_clean_text,
)
from databank_mlops.components.transformation.preprocessors.field_number_to_string import (
    mb_clean_cat_number,
)
from databank_mlops.app.db.models.model import (
    DriftFeatures,
    DriftTarget,
    ModelPerfomance,
)
from databank_mlops.app.db.db import get_db_session
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from evidently.legacy.metrics import ColumnDriftMetric, ClassificationQualityMetric
from evidently.legacy.metric_preset import TargetDriftPreset
from evidently.legacy.calculations.stattests import psi_stat_test
from evidently.legacy.report import Report
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from dotenv import load_dotenv
from datetime import datetime
import mlflow

load_dotenv()


def obtener_monitoreo(**context):
    """ """
    cat_cols = ["OCCUPATION"]

    cat_num_cols = [
        "AGE",
        "ANNUAL_INCOME",
        "NUM_OF_LOAN",
        "NUM_OF_DELAYED_PAYMENT",
        "CHANGED_CREDIT_LIMIT",
        "OUTSTANDING_DEBT",
        "AMOUNT_INVESTED_MONTHLY",
        "MONTHLY_BALANCE",
    ]

    num_cols = [
        "MONTHLY_INHAND_SALARY",
        "NUM_BANK_ACCOUNTS",
        "NUM_CREDIT_CARD",
        "INTEREST_RATE",
        "DELAY_FROM_DUE_DATE",
        "NUM_CREDIT_INQUIRIES",
        "CREDIT_UTILIZATION_RATIO",
        "TOTAL_EMI_PER_MONTH",
    ]

    pl_clean = ColumnTransformer(
        [
            (
                "prep_cat",
                Pipeline([("mb_clean_text", mb_clean_text("MISSING"))]),
                cat_cols,
            ),
            #
            (
                "prep_cat_num",
                Pipeline(
                    [
                        ("mb_clean_text_number", mb_clean_text_number()),
                        ("mb_clean_cat_number", mb_clean_cat_number()),
                    ]
                ),
                cat_num_cols,
            ),
            #
            (
                "prep_num",
                Pipeline([("mb_clean_cat_number", mb_clean_cat_number())]),
                num_cols,
            ),
        ],
        remainder="passthrough",
        force_int_remainder_cols=False,
        verbose_feature_names_out=False,
    )

    df = pd.read_csv(r"/opt/airflow/dags/train.csv", low_memory=False)
    df.columns = df.columns.str.upper()

    model = mlflow.sklearn.load_model(r"models:/XGBClassifier@production")
    prediction = model.predict_proba(df)[:, 1].squeeze()
    target_real = np.where((df.CREDIT_SCORE == "Poor"), 1, 0)

    index_columns = [c for c in PredictRequest.model_fields.keys() if c != "ID"]
    df = df.loc[:, index_columns]
    df["PD"] = prediction
    df["TARGET"] = target_real

    index_reference = np.random.choice(
        np.arange(0, df.shape[0]), int(np.floor(df.shape[0] * 0.5)), replace=True
    )
    df_reference = df.iloc[index_reference, :]

    index_current = np.random.choice(
        np.arange(0, df.shape[0]), int(np.floor(df.shape[0] * 0.2)), replace=True
    )
    df_current = df.iloc[index_current, :]
    df_current["AGE"] = 33

    df_reference = pl_clean.fit_transform(df_reference)
    df_reference = pd.DataFrame(df_reference, columns=pl_clean.get_feature_names_out())
    df_reference["PD"] = df_reference.PD.astype(np.float64)
    df_reference["TARGET"] = df_reference.TARGET.astype(np.int64)

    df_current = pl_clean.transform(df_current)
    df_current = pd.DataFrame(df_current, columns=pl_clean.get_feature_names_out())
    df_current["PD"] = df_current.PD.astype(np.float64)
    df_current["TARGET"] = df_current.TARGET.astype(np.int64)

    # Se calculan PSIs (Drift1 data)
    ls_metrics_psi = [
        ColumnDriftMetric(column_name=c, stattest=psi_stat_test) for c in index_columns
    ]
    report = Report(metrics=ls_metrics_psi)
    report.run(reference_data=df_reference, current_data=df_current)
    report = report.as_dict()
    #
    datetime_ref = datetime.utcnow()
    for rep in report["metrics"]:
        drif_column = DriftFeatures(
            feature=rep["result"]["column_name"],
            drift=(1 * rep["result"]["drift_detected"]),
            timestamp=datetime_ref,
        )
        with get_db_session() as db:
            db.add(drif_column)

    report2 = Report(metrics=[ClassificationQualityMetric(probas_threshold=0.5)])
    column_mapping = ColumnMapping(target="TARGET", prediction="PD", pos_label=1)
    report2.run(
        reference_data=df_reference,
        current_data=df_current,
        column_mapping=column_mapping,
    )
    report2 = report2.as_dict()
    #
    datetime_ref = datetime.utcnow()
    for metric, value in report2["metrics"][0]["result"]["current"].items():
        model_performance = ModelPerfomance(
            metric=metric, value=float(value), timestamp=datetime_ref
        )
        with get_db_session() as db:
            db.add(model_performance)

    column_mapping = ColumnMapping(
        target="TARGET",
    )
    report3 = Report(
        metrics=[
            TargetDriftPreset(stattest=psi_stat_test),
        ]
    )
    report3.run(
        reference_data=df_reference,
        current_data=df_current,
        column_mapping=column_mapping,
    )
    report3 = report3.as_dict()
    rep = report3["metrics"][0]

    drif_column = DriftTarget(
        drift=(1 * rep["result"]["drift_detected"]), timestamp=datetime.utcnow()
    )
    with get_db_session() as db:
        db.add(drif_column)


with DAG(
    dag_id="dag_monitoreo",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["monitoreo"],
) as dag:
    monitoreo = PythonOperator(task_id="monitoreo", python_callable=obtener_monitoreo)

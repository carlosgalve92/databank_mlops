import pandas as pd
from sklearn.metrics import roc_auc_score, f1_score, recall_score, precision_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import pathlib
import numpy as np
from dotenv import load_dotenv

from databank_mlops.entity.config_entity import ModelEvaluationConfig
from databank_mlops.utils.common import load_bin, save_json

load_dotenv()


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self, actual, pred, threshold=0.5):
        gini = roc_auc_score(actual, pred)
        f1 = f1_score(actual, np.where(pred > threshold, 1, 0))
        recall = recall_score(actual, np.where(pred > threshold, 1, 0))
        precision = precision_score(actual, np.where(pred > threshold, 1, 0))

        return {"gini": gini, "f1": f1, "recall": recall, "precision": precision}

    def read_files(self, train_data_path, test_data_path, target_column):
        """ """
        train_data = pd.read_csv(train_data_path)
        test_data = pd.read_csv(test_data_path)

        self.train_x = train_data.drop([target_column], axis=1)
        self.train_y = train_data[[target_column]]

        self.test_x = test_data.drop([target_column], axis=1)
        self.test_y = test_data[[target_column]]

    def log_into_mlflow(self, path_model, local_metrics_file, model_name, version):
        model = load_bin(
            pathlib.Path(path_model).joinpath(f"{model_name}__{version}.joblib")
        )

        # mlflow.set_registry_uri(self.config.mlflow_uri)
        mlflow.set_experiment(f"Experimentos modelo {model_name}: {version}")
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            train_pred_y = model.predict_proba(self.train_x)
            test_pred_y = model.predict_proba(self.test_x)

            dict_metrics = {}

            dict_metrics.update(
                {
                    f"{k}_train": v
                    for k, v in self.eval_metrics(
                        self.train_y, train_pred_y[:, 1]
                    ).items()
                }
            )

            dict_metrics.update(
                {
                    f"{k}_test": v
                    for k, v in self.eval_metrics(
                        self.test_y, test_pred_y[:, 1]
                    ).items()
                }
            )

            save_json(local_metrics_file, dict_metrics)

            mlflow.log_metrics(dict_metrics)

            mlflow.log_params(model.get_params())

            # Model registry does not work with file store
            if tracking_url_type_store != "file":
                # Register the model
                # There are other ways to use the Model Registry, which depends on the use case,
                # please refer to the doc for more information:
                # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                mlflow.sklearn.log_model(
                    model,
                    artifact_path=f"{model_name}",
                    registered_model_name=rf"{model_name}",
                    pip_requirements=["sklearn", "xgboost"],
                    signature=mlflow.models.infer_signature(
                        self.train_x.values, train_pred_y
                    ),
                )
            else:
                mlflow.sklearn.log_model(model, "model")

        client = mlflow.tracking.MlflowClient()

        client.update_registered_model(
            name=rf"{model_name}",
            description=f"Modelo {model_name} orientado a la originacion de creditos",
        )

        #
        versions = client.search_model_versions(f"name='{model_name}'")
        #
        latest_version = versions[0].version
        client.set_model_version_tag(model_name, latest_version, "status", "active")
        client.set_registered_model_alias(model_name, "production", latest_version)
        client.update_model_version(
            name=rf"{model_name}",
            version=latest_version,
            description=f"Version {latest_version} del modelo {model_name}",
        )

        for v in versions[1:]:
            for key, value in v.tags.items():
                client.set_model_version_tag(
                    model_name, v.version, "status", "archived"
                )

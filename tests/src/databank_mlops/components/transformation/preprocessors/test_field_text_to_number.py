import pytest
import numpy as np
import pandas as pd
from databank_mlops.components.transformation.preprocessors.field_text_to_number import (
    mb_clean_text_number,
)


@pytest.fixture
def dataframe():
    # Crear datos de prueba con pandas
    data = {
        "feature_1": ["_1_000", "_1.81531", "-500", "_163.13", "12,331.13", "121314"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def p_mb_clean_text_number():
    return mb_clean_text_number()


def test_fit_transform(p_mb_clean_text_number, dataframe):
    df_test = p_mb_clean_text_number.fit_transform(dataframe)
    assert (
        df_test.values.squeeze()
        == np.asarray([1000, 1.81531, -500, 163.13, 12331.13, 121314])
    ).all()

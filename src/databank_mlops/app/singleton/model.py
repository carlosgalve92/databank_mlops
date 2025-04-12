from functools import lru_cache
from databank_mlops.utils.common import read_yaml
from databank_mlops.constants import CONFIG_FILE_PATH
import mlflow

config_production = read_yaml(CONFIG_FILE_PATH).production


@lru_cache(maxsize=1)
def load_model(
    model_name=config_production.model_name, model_alias=config_production.model_alias
):
    model_uri = rf"models:/{model_name}@{model_alias}"

    return mlflow.sklearn.load_model(model_uri)

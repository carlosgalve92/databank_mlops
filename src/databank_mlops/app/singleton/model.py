from functools import lru_cache
from databank_mlops.models.registry import ModelRegistry
from databank_mlops.models.factory import ModelFactory


@lru_cache(maxsize=1)
def get_model_factory() -> ModelFactory:
    registry = ModelRegistry()
    return ModelFactory(registry)

import joblib


dict_registry = {
    "model1": {
        "latest": {
            "model": "Logistic Regression",
            "path": "./models/logistic_regresion_v1.joblib",
        }
    }
}


class ModelRegistry:
    def __init__(self, registry: dict = dict_registry):
        self.registry = registry

    def load_model(self, model_name: str, model_version: str = "latest"):
        """ """
        if model_name not in self.registry:
            raise KeyError(f"Modelo '{model_name}' no encontrado.")

        model_path = self.registry.get(model_name).get(model_version).get("path")

        return joblib.load(model_path)

from fastapi import APIRouter, HTTPException, Depends, Query
import pandas as pd
from databank_mlops.app.schemas.predict import PredictRequest, PredictResponse
from databank_mlops.app.singleton.model import get_model_factory
from databank_mlops.models.factory import ModelFactory


router = APIRouter()


# Endpoint para hacer la predicción
@router.post("/predict", response_model=PredictResponse)
async def predict(
    request: PredictRequest,
    model_factory: ModelFactory = Depends(get_model_factory),
    model_name: str = Query(...),
    model_version: str = Query("latest"),
):
    try:
        # Instanciamos el predictor que hace la inferencia
        model = model_factory.get_model(model_name, model_version)

        # Extraemos las características del request y llamamos al método
        # predict
        prediction = model.predict_proba(pd.DataFrame([request.dict()]))[:, 1].squeeze()

        # Retornamos la respuesta con el esquema
        return PredictResponse(prediction=prediction)

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error during prediction: {str(e)}"
        )


if __name__ == "__main__":
    results = predict(
        PredictRequest(feature1=2.0, feature2=3.1, feature3=4.5),
        model_name="model1",
        model_version="latest",
    )

    print("stop")

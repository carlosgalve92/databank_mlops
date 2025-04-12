from fastapi import APIRouter, HTTPException, Depends
import pandas as pd
from databank_mlops.app.schemas.predict import PredictRequest, PredictResponse
from databank_mlops.app.singleton.model import load_model
from typing import Any

router = APIRouter()


# Endpoint para hacer la predicción
@router.post("/predict", response_model=PredictResponse)
async def predict(
    request: PredictRequest,
    model: Any = Depends(load_model),
):
    try:
        # Extraemos las características del request y llamamos al método
        # predict
        prediction = model.predict_proba(pd.DataFrame([request.dict()]))[:, 1].squeeze()

        # Retornamos la respuesta con el esquema
        return PredictResponse(prediction=prediction)

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error during prediction: {str(e)}"
        )

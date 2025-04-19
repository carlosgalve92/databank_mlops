from fastapi import APIRouter, HTTPException, Depends
import pandas as pd
from databank_mlops.app.schemas.predict import PredictRequest, PredictResponse
from databank_mlops.app.singleton.model import load_model
from databank_mlops.app.db.db import get_db
from databank_mlops.app.db.models.model import PredictionData
from typing import Any

router = APIRouter()


# Endpoint para hacer la predicción
@router.post("/predict", response_model=PredictResponse)
async def predict(
    request: PredictRequest, model: Any = Depends(load_model), db=Depends(get_db)
):
    try:
        #
        df = pd.DataFrame([request.dict()])
        #
        prediction = model.predict_proba(df)[:, 1].squeeze()
        prediction = PredictResponse(prediction=prediction)
        #
        data = PredictionData.from_pydantic(request, prediction)
        db.add(data)
        db.commit()
        db.refresh(data)
        # Retornamos la respuesta con el esquema
        return prediction

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error during prediction: {str(e)}"
        )

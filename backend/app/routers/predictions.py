from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from app.ml.predict import predict

router = APIRouter(prefix="/predictions", tags=["predictions"])

@router.post("/", response_model=schemas.PredictionResponse, status_code=201)
def create_prediction(
    payload: schemas.PredictionRequest,
    db: Session = Depends(get_db)
):
    features = payload.model_dump()
    result = predict(features)
    db_pred = crud.create_prediction(db, input_features=features, result=result)
    return db_pred

@router.get("/", response_model=list[schemas.PredictionResponse])
def list_predictions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_predictions(db, skip=skip, limit=limit)

@router.get("/stats", response_model=schemas.ModelStats)
def get_stats(db: Session = Depends(get_db)):
    return crud.get_model_stats(db)
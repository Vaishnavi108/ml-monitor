from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud
from app.ml.drift import compute_drift

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}

@router.get("/stats")
def model_stats(db: Session = Depends(get_db)):
    return crud.get_model_stats(db)

@router.get("/drift")
def drift_report(db: Session = Depends(get_db)):
    """Run drift detection on demand and return full report."""
    return compute_drift(db)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/health")
def health_check():
    """Used by Docker health checks and load balancers."""
    return {"status": "ok", "version": "1.0.0"}

@router.get("/stats")
def model_stats(db: Session = Depends(get_db)):
    return crud.get_model_stats(db)
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app import models, schemas

def create_prediction(db: Session, input_features: dict, result: dict) -> models.Prediction:
    db_pred = models.Prediction(
        input_features=input_features,
        prediction=result["prediction"],
        label=result["label"],
        confidence=result["confidence"],
        probabilities=result["probabilities"],
    )
    db.add(db_pred)
    db.commit()
    db.refresh(db_pred)
    return db_pred

def get_predictions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Prediction)\
             .order_by(models.Prediction.created_at.desc())\
             .offset(skip).limit(limit).all()

def get_model_stats(db: Session) -> dict:
    total = db.query(func.count(models.Prediction.id)).scalar()
    positive = db.query(func.count(models.Prediction.id))\
                 .filter(models.Prediction.prediction == 1).scalar()
    avg_conf = db.query(func.avg(models.Prediction.confidence)).scalar()

    cutoff = datetime.utcnow() - timedelta(hours=24)
    last_24h = db.query(func.count(models.Prediction.id))\
                 .filter(models.Prediction.created_at >= cutoff).scalar()

    return {
        "total_predictions": total or 0,
        "positive_rate": round((positive / total) if total else 0, 4),
        "avg_confidence": round(avg_conf or 0, 4),
        "predictions_last_24h": last_24h or 0,
    }
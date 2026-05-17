from sqlalchemy import Column, Integer, Float, String, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    # Input features stored as JSON — flexible for future model changes
    input_features = Column(JSON, nullable=False)
    prediction = Column(Integer, nullable=False)      # 0 or 1
    label = Column(String, nullable=False)            # "<=50K" or ">50K"
    confidence = Column(Float, nullable=False)
    probabilities = Column(JSON, nullable=False)
    model_version = Column(String, default="1.0.0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ModelMetric(Base):
    __tablename__ = "model_metrics"

    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String, nullable=False)      # e.g. "accuracy", "drift_score"
    metric_value = Column(Float, nullable=False)
    window = Column(String, nullable=False)           # e.g. "last_100", "daily"
    computed_at = Column(DateTime(timezone=True), server_default=func.now())
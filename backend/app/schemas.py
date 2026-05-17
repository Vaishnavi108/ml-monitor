from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PredictionRequest(BaseModel):
    age: float = Field(..., ge=17, le=90, description="Age in years")
    education_num: float = Field(..., ge=1, le=16)
    hours_per_week: float = Field(..., ge=1, le=99)
    capital_gain: float = Field(0.0, ge=0)
    capital_diff: float = Field(0.0)

    class Config:
        json_schema_extra = {
            "example": {
                "age": 35,
                "education_num": 13,
                "hours_per_week": 40,
                "capital_gain": 0,
                "capital_diff": 0
            }
        }

class PredictionResponse(BaseModel):
    id: int
    prediction: int
    label: str
    confidence: float
    probabilities: dict
    model_version: str
    created_at: datetime

    class Config:
        from_attributes = True

class MetricResponse(BaseModel):
    metric_name: str
    metric_value: float
    window: str
    computed_at: datetime

class ModelStats(BaseModel):
    total_predictions: int
    positive_rate: float        # % predicted >50K
    avg_confidence: float
    predictions_last_24h: int
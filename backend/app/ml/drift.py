import numpy as np
from scipy import stats
from sqlalchemy.orm import Session
from app.models import Prediction, ModelMetric
from app.database import SessionLocal
import pickle
import pandas as pd
from pathlib import Path

FEATURE_NAMES = [
    "age", "education_num", "hours_per_week",
    "capital_gain", "capital_diff"
]

REFERENCE_STATS = {
    "age":            {"mean": 38.6, "std": 13.6, "min": 17, "max": 90},
    "education_num":  {"mean": 10.1, "std": 2.6,  "min": 1,  "max": 16},
    "hours_per_week": {"mean": 40.4, "std": 12.3, "min": 1,  "max": 99},
    "capital_gain":   {"mean": 1078, "std": 7385,  "min": 0,  "max": 99999},
    "capital_diff":   {"mean": 894,  "std": 7506,  "min": -4356, "max": 99999},
}

def compute_drift(db: Session) -> dict:
    """
    Fetch last 100 predictions, run KS test on each feature,
    return drift scores and whether drift is detected.
    """
    preds = db.query(Prediction)\
              .order_by(Prediction.created_at.desc())\
              .limit(100).all()

    if len(preds) < 10:
        return {"status": "insufficient_data", "min_required": 10, "current": len(preds)}

    results = {}
    drift_detected = False

    for feature in FEATURE_NAMES:
        values = [p.input_features.get(feature, 0) for p in preds]
        values = np.array(values, dtype=float)

        ref = REFERENCE_STATS[feature]
        ref_samples = np.random.normal(
            loc=ref["mean"],
            scale=ref["std"],
            size=500
        )
        ref_samples = np.clip(ref_samples, ref["min"], ref["max"])

        ks_stat, p_value = stats.ks_2samp(values, ref_samples)

        drifted = p_value < 0.05
        if drifted:
            drift_detected = True

        results[feature] = {
            "ks_statistic": round(float(ks_stat), 4),
            "p_value": round(float(p_value), 4),
            "drift_detected": drifted,
            "current_mean": round(float(values.mean()), 2),
            "reference_mean": ref["mean"],
        }

    return {
        "status": "completed",
        "sample_size": len(preds),
        "drift_detected": drift_detected,
        "features": results,
    }

def save_drift_metric(db: Session, drift_report: dict):
    """Persist drift score to model_metrics table."""
    if drift_report.get("status") != "completed":
        return

    drifted_count = sum(
        1 for f in drift_report["features"].values()
        if f["drift_detected"]
    )
    drift_score = drifted_count / len(FEATURE_NAMES)

    metric = ModelMetric(
        metric_name="drift_score",
        metric_value=drift_score,
        window="last_100"
    )
    db.add(metric)
    db.commit()

def run_drift_check():
    """Entry point called by the scheduler."""
    db = SessionLocal()
    try:
        print("Running drift check...")
        report = compute_drift(db)
        save_drift_metric(db, report)
        if report.get("drift_detected"):
            print(f"⚠️  DRIFT DETECTED: {report}")
        else:
            print(f"✅ No drift detected. Sample size: {report.get('sample_size')}")
    finally:
        db.close()
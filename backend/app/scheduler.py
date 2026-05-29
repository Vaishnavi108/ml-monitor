from apscheduler.schedulers.background import BackgroundScheduler
from app.ml.drift import run_drift_check

scheduler = BackgroundScheduler()

def start_scheduler():
    """Start background drift detection job."""
    scheduler.add_job(
        run_drift_check,
        trigger="interval",
        minutes=60,
        id="drift_check",
        replace_existing=True
    )
    scheduler.start()
    print("Scheduler started — drift check runs every 60 minutes")

def stop_scheduler():
    """Graceful shutdown."""
    if scheduler.running:
        scheduler.shutdown()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import predictions, metrics

# Create all tables on startup (Alembic handles this in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ML Model Monitor",
    description="Real-time monitoring API for ML model predictions",
    version="1.0.0",
    docs_url="/docs",       # Swagger UI — free with FastAPI
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predictions.router, prefix="/api/v1")
app.include_router(metrics.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "ML Monitor API", "docs": "/docs"}
from __future__ import annotations

from pathlib import Path
from typing import Dict

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

APP_DIR = Path(__file__).resolve().parent
MODEL_PATH = APP_DIR.parent / "artifacts" / "demo_model.joblib"
FEATURE_NAMES = ["temperature", "humidity", "pressure"]

app = FastAPI(
    title="NeuroForge ML Inference Service",
    version="0.1.0",
    description="Demonstration inference API. The synthetic model is not suitable for real-world decisions.",
)


class PredictionRequest(BaseModel):
    features: Dict[str, float] = Field(
        examples=[{"temperature": 22.5, "humidity": 61.0, "pressure": 1012.4}]
    )


class PredictionResponse(BaseModel):
    prediction: float
    model_version: str
    disclaimer: str


def build_demo_model() -> Pipeline:
    """Train a deterministic synthetic regression model for smoke testing only."""
    rng = np.random.default_rng(42)
    x = np.column_stack(
        [
            rng.uniform(0, 40, 600),
            rng.uniform(10, 100, 600),
            rng.uniform(970, 1040, 600),
        ]
    )
    y = 0.35 * x[:, 0] + 0.08 * x[:, 1] + 0.015 * (x[:, 2] - 1000) + 2.0
    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("regressor", RandomForestRegressor(n_estimators=80, random_state=42)),
        ]
    )
    model.fit(x, y)
    return model


def load_model():
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return build_demo_model()


model = load_model()


@app.get("/health")
def health():
    return {"status": "healthy", "service": "ml-inference", "model_version": "demo-0.1.0"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if set(request.features) != set(FEATURE_NAMES):
        raise HTTPException(
            status_code=422,
            detail={"required_features": FEATURE_NAMES, "received_features": sorted(request.features)},
        )

    values = np.array([[request.features[name] for name in FEATURE_NAMES]], dtype=float)
    if not np.isfinite(values).all():
        raise HTTPException(status_code=422, detail="All feature values must be finite numbers.")

    prediction = float(model.predict(values)[0])
    return PredictionResponse(
        prediction=prediction,
        model_version="demo-0.1.0",
        disclaimer="Synthetic demonstration model only; not validated for operational or safety-critical use.",
    )

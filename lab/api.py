"""Local educational demo API. No patient diagnosis or clinical use."""
from functools import lru_cache
from math import isfinite
from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app=FastAPI(title="Interdisciplinary AI Teaching API",description="Experimental classroom API. Not for patient care.")
class PredictionRequest(BaseModel):
    features: dict[str,float] = Field(min_length=1)
@lru_cache

def load_bundle():
    path=Path("artifacts/model.joblib")
    if not path.exists():
        raise FileNotFoundError("Train a model first: python -m lab.train ...")
    return joblib.load(path)  # trusted local artifact only
@app.get("/health")
def health():
    return {"status":"ok","model_available":Path("artifacts/model.joblib").exists()}
@app.post("/predict")
def predict(payload: PredictionRequest):
    try:
        bundle=load_bundle()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503,detail=str(exc)) from exc
    required=set(bundle["features"])
    if set(payload.features)!=required:
        raise HTTPException(status_code=422,detail={"missing":sorted(required-set(payload.features)),"unexpected":sorted(set(payload.features)-required)})
    x=pd.DataFrame([{name:payload.features[name] for name in bundle["features"]}])
    if not all(isfinite(v) for v in payload.features.values()):
        raise HTTPException(status_code=422,detail="Features must be finite numbers")
    prediction=str(bundle["model"].predict(x)[0]);proba=bundle["model"].predict_proba(x)[0]
    return {"predicted_subtype":prediction,"probabilities":{str(k):round(float(v),4) for k,v in zip(bundle["model"].classes_,proba)},"disclaimer":"Synthetic classroom demo; not a diagnosis or validated biomarker"}

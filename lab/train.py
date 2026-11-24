"""Train baseline and tuned model on the same fixed holdout split."""
import argparse
import json
from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, classification_report, confusion_matrix, f1_score, roc_auc_score
from sklearn.model_selection import GridSearchCV, train_test_split, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

LABELS = ("LUAD", "LUSC")
EXCLUDED = {"label", "sample_id", "patient_id", "case_id", "submitter_id"}

def validate(df: pd.DataFrame):
    if "label" not in df:
        raise ValueError("CSV must include label column")
    if df["label"].isna().any() or set(df["label"].unique()) != set(LABELS):
        raise ValueError("This example expects both LUAD and LUSC labels only")
    if "sample_id" in df and df["sample_id"].duplicated().any():
        raise ValueError("Duplicate sample IDs: reconcile patient/sample provenance first")
    features = [c for c in df.columns if c not in EXCLUDED]
    if not features:
        raise ValueError("No features found")
    if any(not pd.api.types.is_numeric_dtype(df[c]) for c in features):
        raise ValueError("All predictor features must be numeric")
    if df["label"].value_counts().min() < 10:
        raise ValueError("At least 10 examples of each class required for this demo")
    if df[features].isna().all(axis=0).any():
        raise ValueError("Completely empty feature column detected")
    return features

def train(data: str, out: str):
    df = pd.read_csv(data)
    features = validate(df)
    if "patient_id" in df and df["patient_id"].duplicated().any():
        raise ValueError("Repeated patients detected: implement group-aware split before using this data")
    x, y = df[features], df["label"]
    indices = list(range(len(df)))
    tr, te = train_test_split(indices, test_size=0.2, random_state=42, stratify=y)
    xtr, xte, ytr, yte = x.iloc[tr], x.iloc[te], y.iloc[tr], y.iloc[te]
    base = Pipeline([("imputer", SimpleImputer(strategy="median")),("scaler", StandardScaler()),("model", LogisticRegression(max_iter=2000, random_state=42))])
    tuned = Pipeline([("imputer", SimpleImputer(strategy="median")),("model", RandomForestClassifier(random_state=42, n_jobs=1))])
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    search = GridSearchCV(tuned, {"model__max_depth":[3, None],"model__min_samples_leaf":[1, 3]}, cv=cv, scoring="balanced_accuracy", n_jobs=1)
    models = {"baseline": base.fit(xtr, ytr), "tuned": search.fit(xtr, ytr).best_estimator_}
    scores = {}
    for name, model in models.items():
        pred = model.predict(xte)
        prob = model.predict_proba(xte)[:, list(model.classes_).index("LUSC")]
        scores[name] = {"accuracy":float(accuracy_score(yte,pred)), "balanced_accuracy":float(balanced_accuracy_score(yte,pred)),"macro_f1":float(f1_score(yte,pred,average="macro")),"roc_auc_lusc":float(roc_auc_score((yte=="LUSC").astype(int),prob)),"confusion_matrix_LUAD_LUSC":confusion_matrix(yte,pred,labels=LABELS).tolist(),"classification_report": classification_report(yte,pred,output_dict=True,zero_division=0)}
    target=Path(out); target.mkdir(parents=True,exist_ok=True)
    joblib.dump({"model":models["tuned"], "features":features, "labels":LABELS,"note":"Research demonstration only, never for clinical use"},target/"model.joblib")
    joblib.dump({"model":models["baseline"], "features":features,"labels":LABELS},target/"baseline.joblib")
    (target/"metrics.json").write_text(json.dumps({"metrics":scores,"best_parameters":search.best_params_,"holdout_size":len(te),"dataset":str(data),"warning":"Evaluation uses synthetic data unless explicitly replaced; holdout is not external validation"},indent=2))
    # Holdout indices are recorded to demonstrate evaluation without evaluating on training records.
    (target/"holdout_indices.json").write_text(json.dumps(te))
    print(json.dumps({"metrics":{k:{m:v for m,v in d.items() if m in ("accuracy","balanced_accuracy","macro_f1","roc_auc_lusc")} for k,d in scores.items()},"best_parameters":search.best_params_},indent=2))

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--data",required=True);p.add_argument("--out",default="artifacts");a=p.parse_args();train(a.data,a.out)

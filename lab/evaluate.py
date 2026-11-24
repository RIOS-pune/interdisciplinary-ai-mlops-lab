"""Reproduce the held-out metrics using recorded split indices; never training rows."""
import argparse
import json
from pathlib import Path
import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, balanced_accuracy_score

def evaluate(data: str, model_path: str):
    path=Path(model_path)
    bundle=joblib.load(path)  # load only artifacts you have created/trust
    indices=json.loads((path.parent/"holdout_indices.json").read_text())
    df=pd.read_csv(data).iloc[indices]
    pred=bundle["model"].predict(df[bundle["features"]])
    result={"balanced_accuracy":float(balanced_accuracy_score(df["label"],pred)),"confusion_matrix_LUAD_LUSC":confusion_matrix(df["label"],pred,labels=["LUAD","LUSC"]).tolist(),"report":classification_report(df["label"],pred,output_dict=True,zero_division=0)}
    print(json.dumps(result,indent=2))
    return result
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--data",required=True);p.add_argument("--model",required=True);a=p.parse_args();evaluate(a.data,a.model)

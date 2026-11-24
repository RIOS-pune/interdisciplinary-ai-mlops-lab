"""Generate intentionally artificial gene-like measurements, never biological claims."""
from pathlib import Path
import numpy as np
import pandas as pd

FEATURES = ["GENE_A", "GENE_B", "GENE_C", "GENE_D", "GENE_E", "GENE_F"]

def generate(n: int = 300, seed: int = 42) -> pd.DataFrame:
    if n < 20:
        raise ValueError("n must be at least 20")
    rng = np.random.default_rng(seed)
    labels = np.array(["LUAD", "LUSC"] * (n // 2) + (["LUAD"] if n % 2 else []))
    rng.shuffle(labels)
    x = rng.normal(loc=5, scale=1.1, size=(n, len(FEATURES)))
    x[labels == "LUAD", 0] += 1.3
    x[labels == "LUAD", 2] += 0.7
    x[labels == "LUSC", 1] += 1.4
    x[labels == "LUSC", 4] += 0.8
    df = pd.DataFrame(x, columns=FEATURES)
    df.insert(0, "sample_id", [f"SYN-{i:04d}" for i in range(n)])
    df["label"] = labels
    return df

if __name__ == "__main__":
    destination = Path("data/synthetic/expression_demo.csv")
    destination.parent.mkdir(parents=True, exist_ok=True)
    df = generate()
    df.to_csv(destination, index=False)
    print(f"Generated {len(df)} synthetic samples at {destination}")

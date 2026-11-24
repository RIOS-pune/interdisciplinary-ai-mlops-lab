from lab.generate_synthetic import generate
from lab.train import validate, train
import json

def test_data_generation():
    data=generate(100)
    assert len(data)==100
    assert set(data.label)=={"LUAD","LUSC"}
    assert len(validate(data))==6

def test_training_pipeline(tmp_path):
    data=tmp_path/"demo.csv"
    generate(120).to_csv(data,index=False)
    artifacts=tmp_path/"out"
    train(str(data),str(artifacts))
    stats=json.loads((artifacts/"metrics.json").read_text())
    assert set(stats["metrics"])=={"baseline","tuned"}
    assert stats["holdout_size"]==24

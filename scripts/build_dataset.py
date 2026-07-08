import json
from dataclasses import asdict

from pipeline.dataset_builder.builder import DatasetBuilder
from pipeline.postprocess.subquestion_expander import SubQuestionExpander
from pipeline.models.question import Question


INPUT="output/json/final_dataset.json"
OUTPUT="dataset/json/dataset_v1.json"

with open(INPUT,"r",encoding="utf8") as f:
    raw=json.load(f)

questions=[]

for x in raw:
    q=Question()

    for k,v in x.items():
        if hasattr(q,k):
            setattr(q,k,v)

    questions.append(q)

questions=SubQuestionExpander().expand(questions)

dataset=DatasetBuilder().build(questions)

import os
os.makedirs("dataset/json",exist_ok=True)

with open(OUTPUT,"w",encoding="utf8") as f:
    json.dump(
        [asdict(x) for x in dataset],
        f,
        indent=2,
        ensure_ascii=False
    )

print("Questions :",len(dataset))
print("Saved :",OUTPUT)

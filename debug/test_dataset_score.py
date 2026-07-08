
from validators.engine import ValidatorEngine
from validators.score import DatasetScore

q = {

"id":1,

"question":"Find x"

}

report = ValidatorEngine().validate(q)

print(report)

print()

print(DatasetScore().compute(report))

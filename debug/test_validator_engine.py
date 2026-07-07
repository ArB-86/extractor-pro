
from validators.engine import ValidatorEngine

q = {

"id": 1,

"question": "Find x"

}

engine = ValidatorEngine()

print(engine.validate(q))

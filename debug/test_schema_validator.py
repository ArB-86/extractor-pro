
from validators.schema_validator import SchemaValidator

validator=SchemaValidator()

q={

"id":1,

"question":"Find x"

}

print(validator.validate(q))

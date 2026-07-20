
from validators.schema_validator import SchemaValidator


class ValidatorEngine:

    def __init__(self):

        self.validators = [

            SchemaValidator(),

        ]

    def validate(self, question):

        report = {}

        for validator in self.validators:

            name = validator.__class__.__name__

            report[name] = validator.validate(question)

        return report

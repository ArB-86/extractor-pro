from validators.dataset_validator import DatasetValidator

validator = DatasetValidator()

errors = validator.validate("output/json/jeep203.json")

if errors:
    print("ERRORS:")
    for e in errors:
        print("-", e)
else:
    print("Dataset OK")

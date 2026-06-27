
from pipeline.ai.factory import ModelFactory

model = ModelFactory.create("dummy")

print(

    model.generate(

        "Hello"

    )

)

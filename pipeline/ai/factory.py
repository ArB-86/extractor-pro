
from pipeline.ai.providers.dummy import DummyProvider


class ModelFactory:

    @staticmethod
    def create(name):

        if name=="dummy":

            return DummyProvider()

        raise ValueError(name)

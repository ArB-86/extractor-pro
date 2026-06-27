
from pipeline.ai.providers.base import BaseProvider


class DummyProvider(BaseProvider):

    def generate(
        self,
        prompt,
        image=None,
        **kwargs
    ):

        return {

            "provider":"dummy",

            "response":prompt

        }

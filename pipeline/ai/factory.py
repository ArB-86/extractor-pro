import yaml

from pipeline.ai.providers.vllm import VLLMProvider


def create_model():

    cfg=yaml.safe_load(open("configs/llm.yaml"))

    provider=cfg["provider"]

    if provider=="vllm":

        return VLLMProvider(
            model=cfg["model"],
        )

    raise ValueError(provider)

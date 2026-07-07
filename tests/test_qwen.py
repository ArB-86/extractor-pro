from src.llm import QwenClient
from src.llm.prompt_loader import load_prompt

SYSTEM = load_prompt(
    "src/prompts/system_prompt.txt"
)

client = QwenClient()

print(
    client.generate(
        SYSTEM,
        "Say hello."
    )
)

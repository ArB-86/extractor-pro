from src.llm import QwenClient
from src.parser.json_parser import JSONParser


class BaseExtractor:

    def __init__(self):

        self.llm = QwenClient()

    def run(self, system_prompt, user_prompt):

        response = self.llm.generate(
            system_prompt,
            user_prompt,
        )

        return JSONParser.parse(response)

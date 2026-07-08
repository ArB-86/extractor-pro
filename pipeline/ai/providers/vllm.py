from openai import OpenAI


class VLLMProvider:

    def __init__(
        self,
        base_url="http://127.0.0.1:8000/v1",
        api_key="EMPTY",
        model="Qwen/Qwen3-32B-Instruct",
    ):

        self.model=model

        self.client=OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    def generate(self,prompt):

        r=self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role":"user",
                    "content":prompt,
                }
            ],

            temperature=0.2,

            max_tokens=4096,
        )

        return r.choices[0].message.content

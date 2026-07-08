import requests


class QwenClient:

    def __init__(
        self,
        url="http://127.0.0.1:30000/v1/chat/completions",
        model="/home/jiitcah.05/models/Qwen3-32B",
    ):
        self.url = url
        self.model = model

    def chat(self, prompt: str) -> str:

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an expert OCR correction assistant. "
                        "Correct OCR mistakes only. "
                        "Do NOT summarize. "
                        "Do NOT invent text. "
                        "Preserve formatting."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": 0.0,
            "max_tokens": 4096,
        }

        r = requests.post(self.url, json=payload, timeout=600)
        r.raise_for_status()

        return r.json()["choices"][0]["message"]["content"]
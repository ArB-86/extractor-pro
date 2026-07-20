from pathlib import Path

import yaml


class Config:

    BASE = Path("config")

    @staticmethod
    def load(name: str):

        with open(Config.BASE / f"{name}.yaml", "r") as f:

            return yaml.safe_load(f)

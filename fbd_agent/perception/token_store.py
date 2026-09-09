"""Local storage for Yahoo OAuth2 tokens. Never committed — see .gitignore."""

import json
import time
from pathlib import Path
from typing import Optional

DEFAULT_TOKEN_PATH = Path(__file__).resolve().parent.parent.parent / ".yahoo_tokens.json"


class TokenStore:
    def __init__(self, path: Path = DEFAULT_TOKEN_PATH):
        self.path = path

    def save(self, tokens: dict) -> dict:
        tokens = dict(tokens)
        tokens["obtained_at"] = time.time()
        self.path.write_text(json.dumps(tokens, indent=2))
        return tokens

    def load(self) -> Optional[dict]:
        if not self.path.exists():
            return None
        return json.loads(self.path.read_text())

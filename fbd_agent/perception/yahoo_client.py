"""Yahoo Fantasy Sports API client (OAuth2). Phase 1: read-only.

Read Yahoo's Fantasy Sports API terms of service before extending this beyond
personal, read-only use — restrictions on commercial use apply.
"""

import base64
import time
from dataclasses import dataclass
from urllib.parse import urlencode

import requests

from fbd_agent.perception.token_store import TokenStore

AUTHORIZE_URL = "https://api.login.yahoo.com/oauth2/request_auth"
TOKEN_URL = "https://api.login.yahoo.com/oauth2/get_token"
FANTASY_BASE_URL = "https://fantasysports.yahooapis.com/fantasy/v2"

# Read-only Fantasy Sports scope. Never "fspt-w" (write) in this phase — the
# write guardrail is enforced here, at the OAuth layer, not just in app code.
READ_ONLY_SCOPE = "fspt-r"


@dataclass
class Player:
    player_id: str
    name: str
    position: str
    projected_points: float


@dataclass
class RosterPull:
    league_id: str
    week: int
    players: list


class YahooClient:
    """Thin wrapper over the Yahoo Fantasy Sports API. No write methods — Phase 1
    is read-only by design; write endpoints are out of scope until Phase 4."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        league_id: str,
        redirect_uri: str = "https://localhost:8000/callback",
        token_store: TokenStore = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.league_id = league_id
        self.redirect_uri = redirect_uri
        self.token_store = token_store or TokenStore()

    def build_authorization_url(self, state: str = "fbd-agent") -> str:
        """Step 1 of the auth code flow: send the user here to approve access."""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": READ_ONLY_SCOPE,
            "state": state,
        }
        return f"{AUTHORIZE_URL}?{urlencode(params)}"

    def _basic_auth_header(self) -> str:
        raw = f"{self.client_id}:{self.client_secret}".encode()
        return base64.b64encode(raw).decode()

    def _post_token_request(self, data: dict) -> dict:
        response = requests.post(
            TOKEN_URL,
            headers={
                "Authorization": f"Basic {self._basic_auth_header()}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data=data,
            timeout=15,
        )
        response.raise_for_status()
        return self.token_store.save(response.json())

    def exchange_code_for_tokens(self, code: str) -> dict:
        """Step 2: trade the authorization code from the redirect for tokens."""
        return self._post_token_request(
            {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.redirect_uri,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
        )

    def refresh_access_token(self) -> dict:
        tokens = self.token_store.load()
        if tokens is None:
            raise RuntimeError("No stored Yahoo tokens — run the authorization flow first.")
        return self._post_token_request(
            {
                "grant_type": "refresh_token",
                "refresh_token": tokens["refresh_token"],
                "redirect_uri": self.redirect_uri,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
        )

    def _access_token(self) -> str:
        tokens = self.token_store.load()
        if tokens is None:
            raise RuntimeError("No stored Yahoo tokens — run the authorization flow first.")
        if time.time() >= tokens["obtained_at"] + tokens["expires_in"] - 60:
            tokens = self.refresh_access_token()
        return tokens["access_token"]

    def _get(self, path: str) -> dict:
        response = requests.get(
            f"{FANTASY_BASE_URL}/{path}",
            headers={"Authorization": f"Bearer {self._access_token()}"},
            params={"format": "json"},
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    def get_games(self) -> dict:
        """Minimal authenticated read used to verify the OAuth wiring end to end."""
        return self._get("users;use_login=1/games")

    def get_league_settings(self) -> dict:
        raise NotImplementedError("Phase 1: resolve league_key and pull league settings")

    def get_roster(self, week: int) -> RosterPull:
        raise NotImplementedError("Phase 1: pull current roster via the Yahoo API")

    def get_weekly_projections(self, week: int) -> dict:
        raise NotImplementedError("Phase 1: pull weekly projections via the Yahoo API")

"""Yahoo Fantasy Sports API client (OAuth2). Phase 1: read-only.

Read Yahoo's Fantasy Sports API terms of service before extending this beyond
personal, read-only use — restrictions on commercial use apply.
"""

from dataclasses import dataclass


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

    def __init__(self, client_id: str, client_secret: str, league_id: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.league_id = league_id
        # TODO: wire up yahoo_oauth session here.

    def get_league_settings(self) -> dict:
        raise NotImplementedError("Phase 1: pull league settings via the Yahoo API")

    def get_roster(self, week: int) -> RosterPull:
        raise NotImplementedError("Phase 1: pull current roster via the Yahoo API")

    def get_weekly_projections(self, week: int) -> dict:
        raise NotImplementedError("Phase 1: pull weekly projections via the Yahoo API")

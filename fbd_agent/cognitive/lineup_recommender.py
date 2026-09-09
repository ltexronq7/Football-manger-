"""Phase 1 cognitive layer: a single prompt. No planning, no orchestration, no memory."""

from fbd_agent.config import LeagueSettings
from fbd_agent.perception.yahoo_client import Player


def build_lineup_prompt(players: list, settings: LeagueSettings) -> str:
    """Build the one prompt: here are the players, here is the scoring, rank the lineup."""
    player_lines = "\n".join(
        f"- {p.name} ({p.position}), projected {p.projected_points} pts"
        for p in players
    )
    return (
        "League scoring: "
        f"superflex={settings.superflex}, ppr={settings.ppr}, "
        f"passing_td_points={settings.passing_td_points}, "
        f"passing_yards_per_point={settings.passing_yards_per_point}.\n\n"
        f"Players available:\n{player_lines}\n\n"
        "Recommend the optimal starting lineup under this exact scoring."
    )


def recommend_lineup(players: list, settings: LeagueSettings) -> str:
    """Send the single prompt to an LLM and return its lineup recommendation.

    TODO: wire up the actual LLM call (Phase 1 exit criteria: runs on a live week).
    """
    build_lineup_prompt(players, settings)
    raise NotImplementedError("Phase 1: connect this prompt to an LLM call")

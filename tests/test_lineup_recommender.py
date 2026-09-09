from fbd_agent.cognitive.lineup_recommender import build_lineup_prompt
from fbd_agent.config import LeagueSettings
from fbd_agent.perception.yahoo_client import Player


def test_build_lineup_prompt_includes_scoring_and_players():
    settings = LeagueSettings(league_id="123", superflex=True, ppr=1.0)
    players = [Player(player_id="1", name="Test Player", position="QB", projected_points=20.0)]

    prompt = build_lineup_prompt(players, settings)

    assert "superflex=True" in prompt
    assert "Test Player" in prompt

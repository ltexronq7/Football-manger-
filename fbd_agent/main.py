"""Phase 1 entry point: pull -> single prompt -> print. Read-only."""

import os

from dotenv import load_dotenv

from fbd_agent.action.terminal_output import print_lineup_recommendation
from fbd_agent.cognitive.lineup_recommender import recommend_lineup
from fbd_agent.config import DEFAULT_LEAGUE_SETTINGS
from fbd_agent.perception.yahoo_client import YahooClient


def main() -> None:
    load_dotenv()

    client = YahooClient(
        client_id=os.environ["YAHOO_CLIENT_ID"],
        client_secret=os.environ["YAHOO_CLIENT_SECRET"],
        league_id=os.environ["YAHOO_LEAGUE_ID"],
    )

    current_week = 1  # TODO: derive from the live NFL week
    roster = client.get_roster(current_week)
    recommendation = recommend_lineup(roster.players, DEFAULT_LEAGUE_SETTINGS)
    print_lineup_recommendation(current_week, recommendation)


if __name__ == "__main__":
    main()

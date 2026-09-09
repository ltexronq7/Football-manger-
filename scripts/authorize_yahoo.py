"""One-time setup: run the Yahoo OAuth2 authorization code flow and store tokens.

Usage:
    python scripts/authorize_yahoo.py

Prints an authorization URL. Open it, sign in, approve access. Yahoo redirects
to the app's redirect_uri (e.g. https://localhost:8000/callback?code=...) —
nothing is listening there, so the browser will show a connection error, but
the code is in the address bar. Paste the full redirected URL back here.
"""

import os
from urllib.parse import parse_qs, urlparse

from dotenv import load_dotenv

from fbd_agent.perception.yahoo_client import YahooClient


def main() -> None:
    load_dotenv()
    client = YahooClient(
        client_id=os.environ["YAHOO_CLIENT_ID"],
        client_secret=os.environ["YAHOO_CLIENT_SECRET"],
        league_id=os.environ["YAHOO_LEAGUE_ID"],
    )

    print("Open this URL, sign in, and approve access:\n")
    print(client.build_authorization_url())
    print()
    redirected_url = input("Paste the full redirected URL: ").strip()

    code = parse_qs(urlparse(redirected_url).query)["code"][0]
    tokens = client.exchange_code_for_tokens(code)
    print(f"\nStored tokens (expires in {tokens['expires_in']}s).")


if __name__ == "__main__":
    main()

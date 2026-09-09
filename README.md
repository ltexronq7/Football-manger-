# Field of Broken Dreams Agent

A fantasy football lineup recommender built for one specific league's exact scoring
rules — not generic rankings tuned to a different format.

## The wedge

- Superflex slot (Q/W/R/T), no dedicated TE slot
- Full PPR, 1 pt per reception
- 6 points per passing TD, 25 yds/pt
- Fractional and negative scoring on

Generic projections assume 4-pt passing TDs and single-QB rosters. This agent knows
*this* league's math instead.

## Current scope (Phase 0/1)

**Task:** each week, recommend the optimal starting lineup from the current roster,
scored under this league's exact settings. Read-only — no writes to Yahoo.

See [docs/FBD-Agent-Phase-Plan.md](docs/FBD-Agent-Phase-Plan.md) for the full phase
plan and exit criteria.

## Project layout

```
fbd_agent/
  config.py            league scoring settings (the wedge, as data)
  perception/           Yahoo Fantasy Sports API client (OAuth2)
  cognitive/             single-prompt lineup recommender
  action/                 terminal output only — no writes
  storage/                SQLite storage for weekly pulls
  main.py                 entry point
tests/
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in Yahoo API credentials
python -m fbd_agent.main
```

## Guardrails

- No write actions to Yahoo in this phase or the next.
- Any future write action requires an explicit human confirmation step (Phase 4+).

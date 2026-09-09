"""League scoring settings — the wedge, as data.

Values come from the league's actual settings page, not a generic default.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class LeagueSettings:
    league_id: str
    superflex: bool = True
    te_slot: bool = False
    ppr: float = 1.0
    passing_td_points: float = 6.0
    passing_yards_per_point: float = 25.0
    fractional_scoring: bool = True
    negative_scoring: bool = True
    # TODO: fill in from the league's actual roster/settings page via the Yahoo API.
    roster_slots: tuple = field(default_factory=tuple)


DEFAULT_LEAGUE_SETTINGS = LeagueSettings(league_id="")

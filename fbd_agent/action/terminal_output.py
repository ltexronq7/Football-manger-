"""Phase 1 action layer: print to terminal only. No writes to Yahoo — guardrail,
not an oversight. Any write action is out of scope until Phase 4, and even then
stays behind an explicit human confirmation gate."""


def print_lineup_recommendation(week: int, recommendation: str) -> None:
    print(f"=== Week {week} lineup recommendation ===")
    print(recommendation)

# Field of Broken Dreams Agent — Phase Plan

**Built against:** the six-layer agentic stack (Perception → Cognitive → Action → Integration → Operations → Infrastructure)
**Method:** vertical slices, not layer-by-layer
**Started:** September 2026, Week 1 of the season

---

## The wedge

Not "an AI that runs my team." That's what every commodity tool claims, and they all
get league settings wrong.

The wedge is: **an agent that knows *this* league's math.**

- Superflex slot (Q/W/R/T), no dedicated TE slot
- Full PPR, 1 pt per reception
- 6 points per passing TD, 25 yds/pt
- Fractional and negative scoring on

Generic projections are tuned to 4-pt passing TDs and single-QB rosters. In Field of
Broken Dreams, a QB in the superflex is worth far more than any public ranking says.
Every off-the-shelf tool is wrong about your roster in a specific, measurable way. That
gap is the product.

---

## Phase 0 — Define the one task

**Task:** Each week, recommend the optimal starting lineup from the current roster,
scored under this league's exact settings.

Not waivers. Not trades. Not the draft. One task.

**Exit criteria:** You can state the task in one sentence and name what a wrong answer
looks like.

---

## Phase 1 — Thin vertical slice (read-only)

One cut through all six layers. Nothing clever.

| Layer | What gets built |
|---|---|
| Perception | Yahoo Fantasy Sports API (OAuth2). Pull roster, league settings, weekly projections. One source only. |
| Cognitive | A single prompt. No planning, no orchestration, no memory. "Here are the players, here is the scoring, rank the lineup." |
| Action | Print to terminal. **No writes to Yahoo.** |
| Integration | None yet. |
| Operations | None yet. |
| Infrastructure | Local Python. SQLite for stored pulls. |

**Exit criteria:** It runs on a live week and produces a lineup you'd actually consider.

**Note:** Read the Yahoo API terms of service in this phase, not later. There are
restrictions on commercial use that need to be known *before* any business question gets
answered.

---

## Phase 2 — Operations and Integration (the layers that matter)

This is the phase most people skip, and it's the one that makes the project worth
something.

**The eval harness — the single most valuable artifact here.**

Before kickoff each week, log the agent's recommended lineup with a timestamp. After
Monday night, score three numbers:

1. What the agent's lineup would have scored
2. What you actually started
3. The perfect-hindsight optimal lineup

Track the gap over weeks. That's a real, falsifiable performance record — something
almost no agent portfolio project has. Most demos can't be graded. This one grades itself
every seven days.

**Also in this phase:**

- **Traces** — log every prompt, response, latency, and token cost per run
- **Guardrails** — hard block on any write action. Never drop a player. Never submit
  without explicit confirmation.
- **Human-in-the-loop** — recommendation → your approval → only then any action

**Exit criteria:** Four consecutive weeks of scored recommendations in a table you can
show someone.

---

## Phase 3 — Widen

Only after Phases 1 and 2 hold.

- **Perception:** add sources — injury reports, snap counts, opponent defensive rankings,
  Vegas totals
- **Cognitive:** split into separate agents — lineup, waiver scan, trade evaluation —
  with a coordinator
- **Memory:** league-specific patterns. Who overpays for QBs. Who never checks waivers.
  Which owners accept lopsided trades.
- **Integration:** wrap the whole thing as an **MCP server**

The MCP server is the highest-leverage piece in the entire plan. It closes the largest
GH-600 exam gap, produces a public GitHub artifact, and makes the agent callable from
Claude directly instead of living in a terminal.

**Exit criteria:** MCP server public on `github.com/Ltexronq7`.

---

## Phase 4 — Write actions

Only now. Two options:

- Yahoo API write endpoints (add/drop, set lineup), behind a confirmation gate
- Claude in Chrome driving the Yahoo UI, for anything the API won't reach

The guardrail pattern from Phase 2 governs both. Approval gate stays on permanently.

---

## Phase 5 — Answer the selling question

Not before. With four to eight weeks of scored data in hand, the question stops being
speculative.

**The honest read going in:**

Fantasy football AI advice is a crowded market. FantasyPros, Sleeper, ESPN, and a dozen
startups all ship some version of it. Consumer willingness to pay is low, the season is
four months long, and Yahoo's terms may restrict commercial use outright.

So the app is probably not the sellable asset.

**The sellable asset is the evidence.** A public agent with guardrails, traces, an
approval gate, an MCP server, and a scored week-over-week performance record is a
portfolio piece that answers the question every hiring manager actually asks: *can you
build an agent that doesn't just demo well?*

Three possible endpoints, in order of realism:

1. **Portfolio proof** — the strongest and most likely. Pairs directly with GH-600.
2. **Open-source tool** — release it, let league commissioners use it, build reputation.
3. **Commercial product** — lowest probability, gated by Yahoo's terms and a crowded
   field. Revisit only if Phase 2 numbers are genuinely good.

The methodology transfers, too. A read-only agent with human approval gates and a scored
eval harness is exactly the pattern that hospital operations work needs — and that
version has a real buyer.

---

## Build order summary

| Phase | Output | Gate to next phase |
|---|---|---|
| 0 | One-sentence task definition | Task is narrow enough to fail visibly |
| 1 | Working read-only recommender | Ran on a live week |
| 2 | Eval harness + traces + guardrails | 4 weeks of scored results |
| 3 | Multi-source, multi-agent, MCP server | Public repo |
| 4 | Write actions behind approval | Never trips a guardrail |
| 5 | Decision on what to do with it | Made with data, not guesses |

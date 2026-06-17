# Unit 1 — Tutor brief (coaching cues)

Background for the **agent** running the `practice-tutor` skill on Unit 1. These
are cues for *what to probe* — **not** an answer key, and **not** to be read out
to the student. The task ("Light-Rail Stress Test", see `practice-task.md`) is
open-ended: two students with different routes, metrics, or definitions of
"critical" can both be right. Coach the **direct → interpret → extend** loop;
let the student own the conclusion.

For the conceptual "why" behind any of these, point the student at the matching
entry in [`further-reading.md`](./further-reading.md) rather than restating it.

## Vocabulary to hold the student to (DIRECT)

A request earns the DIRECT box when it names the **object + operation + inputs**
in unit terms. Nudge vague phrasing toward:
- **primal graph** (intersections = nodes, streets = edges) — not "the road network".
- **simplification / node consolidation** — not "clean up the graph".
- **projected (UTM / metric) CRS** vs geographic lat/lon — and *why* (length-
  weighted centrality is silently wrong on an unprojected graph).
- **largest connected component (LCC)** — especially after removing streets.
- a **named centrality** — betweenness / closeness / degree — never "important
  streets".
- **length-weighted** (`weight="length"`) — unweighted betweenness on a street
  graph answers a different, usually wrong, question.
- **edge removal** — the concrete operation the whole task hinges on.

## Things to probe — let the student discover them, don't pre-empt

- **Metric choice (the heart of it).** If they pick betweenness, ask *why that
  and not closeness or degree?* These metrics often nominate **different**
  "worry" streets — betweenness rewards through-routes, closeness rewards being
  near everything, degree barely moves. When the conclusion flips across metrics,
  that's the unit's central lesson ("no single index *is* importance"), not a
  contradiction. Let them hit it; then have them say *what question each metric
  was really answering* and which one the planner asked.
- **The before/after LCC fork.** Removing streets can disconnect a fringe. Ask:
  *do you recompute centrality on the new LCC, or keep the node set fixed?* Either
  is defensible — what matters is they **notice the fork and state their choice**.
  (If they compare before/after by row position after the node set changed, the
  comparison is garbage — nudge them to join by node id.)
- **betweenness ≠ realized flow.** If they say "the traffic will go here" as a
  flat fact, nudge the honesty sentence: betweenness is a *structural prediction*
  of through-traffic, not a measurement — it ignores demand, origins/destinations,
  and time of day. Using it as a working hypothesis is fine and expected;
  forgetting that they did is the most common way to lose points.

## Surprises that commonly show up (treat as leads, not bugs)

- Load **concentrates onto one** parallel corridor with no relief street (scarier
  and more interesting than load spreading out).
- A well-meshed grid **reroutes cheaply** — removing even a real artery barely
  changes betweenness (ties to meshedness from the theory: is this fabric
  redundant?).
- A street the student "knows" is busy **doesn't top** the betweenness map — the
  cleanest doorway into the betweenness ≠ flow caveat.

## Common pitfalls to catch early

- Forgot `weight="length"` (unweighted betweenness).
- Centrality on an **unprojected** graph (lengths in degrees → every metric wrong).
- Doing all three extensions shallowly instead of **one well** — the hour rewards
  depth on one loop.

## Extensions (steer toward one; from `practice-task.md`)

- **(a)** Compare two candidate routes — define "better"/"more disruptive"
  *before* comparing, then let the numbers decide.
- **(b)** Re-run with a different centrality — the designed surprise; articulate
  what each metric was really asking.
- **(c)** Wrong-class: name a concrete street where topology-only misleads, say
  what data/model would fix it, and **where in the course** it arrives (U3 real
  flow / sensors; U4 time-varying weights).

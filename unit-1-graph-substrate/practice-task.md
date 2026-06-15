# Unit 1 — Supervised Practice: The Light-Rail Stress Test

**Time: 1 hour, in class, working WITH an AI agent.**
**You will rehearse the loop: DIRECT → INTERPRET → EXTEND.**

> You are advising a city that is about to break ground on a new light-rail
> line. The trains will run down the middle of an existing surface street, and
> those lane-kilometres will **no longer be available to car traffic**. The
> planning office wants one question answered before the design is locked:
>
> **When we take those streets away from cars, which other streets suddenly
> carry the load — and are any of them streets we should worry about?**
>
> Your job is not to give the city a pretty map. It is to make a *defensible
> structural argument* about which streets become more (or less) critical for
> car traffic once the route is removed, and to be honest about the limits of
> what topology alone can tell you.

This is **open-ended on purpose**. There is no single right answer. Two
students who pick different routes, different centralities, or different
definitions of "critical" can both produce defensible work. You are graded on
the **quality of your direct → interpret → extend loop** (see
`rubric.md`), not on matching a key.

---

## What you start from

The demo notebook (`geoai-graph-unit1.ipynb`) already gives you everything you
need on the stack you've been using all session — **OSMnx v2 + pyrosm + igraph
+ folium**, no new heavy dependencies:

- An inline Geofabrik + pyrosm build that produces a **simplified, projected,
  LCC** primal graph for a city.
- `igraph`-backed **betweenness** and **closeness**, plus NetworkX **degree**.
- Top-decile highlight maps (`top_decile_mask`) over folium basemaps.
- The named-street **dual** (`build_named_street_dual`) if you want it.

**Default city: Tel Aviv.** You may pick any city you like (your home town is
encouraged) — just keep it to a bounding box small enough that betweenness
finishes in seconds, the way the demo's Jerusalem cut does.

You are **not** given the prompts to type. Composing the right request, in this
unit's vocabulary, is half the exercise.

---

## The loop, made concrete

Everyone does the **baseline**. Then pick **at least one** extension (a/b/c);
strong students do two. Keep a **decision-log entry per cycle** (copy
`decision-log-template.md` into your working folder).

### Baseline — every student

1. **Build the "before" graph.** Get a clean primal graph of your city:
   simplified, projected to a metric CRS, largest connected component only.
2. **Pick your light-rail route and remove it.** Choose a real surface street
   (or a short chain of connected streets) that a light-rail line could
   plausibly run along. Remove those streets from the graph **as car-routable**
   — i.e. delete the corresponding edges — to get the "after" graph.
   - *Watch the trap:* removing a street can disconnect a fringe of the
     network. Decide explicitly whether you recompute on the new LCC, and say
     so in your log.
3. **Choose a centrality and justify it.** Which measure answers "which streets
   carry car through-traffic"? Name it, and say in one sentence *why* it fits
   this question and not another.
   - *Bridge from the theory:* the conceptually purpose-built "most critical to
     remove" metric is **information centrality** — but the demo's stack computes
     degree / closeness / **betweenness**. So here you **approximate** the
     "critical" question with an explicit **before/after removal** of your route
     and the change in betweenness. (Naming that approximation in your log is
     itself good INTERPRET.)
4. **Compute before and after, and compare.** For your chosen centrality,
   compute it on the before graph and on the after graph. Find the streets
   whose ranking **rises** the most and **falls** the most.
5. **Map it and read it.** Visualise the streets that became more / less
   critical. Then explain, in plain planning language, *what the map is saying*.
6. **Defend your conclusion in one paragraph.** Which streets should the city
   worry about, and on what structural grounds?

### DIRECT / INTERPRET / EXTEND inside the baseline

- **DIRECT** — every request to the agent should name the operation in unit
  vocabulary: *primal graph, simplification, projection / CRS, largest
  connected component, betweenness / closeness / degree centrality, edge
  removal*. If your prompt would read the same for a non-geographer ("find the
  busy streets"), tighten it.
- **INTERPRET** — when the agent hands back a ranked list or a map, restate it
  yourself: *which* streets changed, by *how much*, and whether that matches
  your intuition about the city. A result that surprises you is a lead, not a
  bug to hide.
- **EXTEND** — your baseline finding should raise a new question. Follow it.
  The extensions below are structured leads, but a good question of your own
  counts too.

---

## Extensions (pick at least one)

### (a) Compare two proposals

Pick a **second** candidate route and run the same before/after analysis.
Which of the two proposals is the **better** plan — and what does "better" mean
*structurally*? (Less concentration of load onto a single replacement street?
Fewer high-centrality streets disrupted? Smaller drop in network-wide
accessibility?) State your definition of "better" before you compare, then let
the numbers decide.

### (b) Re-run with a different centrality

Repeat the baseline with a **different** centrality measure (e.g. swap
betweenness for closeness, or add degree). Does your conclusion about "which
streets to worry about" **change**? If it does, that is not a mistake — it
means the two metrics were answering **different questions** all along. Say, in
domain terms, *what question each metric was really answering*, and which one
the planner actually asked.

### (c) Wrong-class — when is a topology-only answer misleading?

Your whole analysis used **structure only** — no traffic counts, no
origins/destinations, no time of day. Construct a concrete situation in your
city where a topology-only answer would **mislead** the planner (hint: a street
that is structurally central but realistically empty, or a structurally minor
street that is jammed every morning). Then articulate **what data or model
class** would be needed to fix it — and where in this course you would expect
to get it. This one is a *meta* question: you are critiquing your own method.

---

## How the hour runs

| Time | What you do |
|---|---|
| 0:00–0:05 | Instructor restates the task + the rubric; you pick your city + route. |
| 0:05–0:45 | Work the loop WITH the agent. Fill a decision-log entry per cycle. |
| 0:45–0:55 | 2–3 students share a **surprising follow-up** they hit. |
| 0:55–1:00 | Instructor synthesis. |

---

## What you hand in

- Your **decision log** (one entry per direct → interpret → extend cycle),
  with the end-of-session rubric check filled in.
- Your **one-paragraph defence** of the baseline conclusion.
- The extension(s) you chose, captured in the log.

You do **not** need a polished notebook for the in-class hour — the log + the
paragraph + your maps are the deliverable. (The take-home `homework.md` asks
for a short writeup.)

---

## A note on prompting (example *structure*, not a script)

You compose your own prompts. As a shape to imitate — not copy — a good DIRECT
request names the object, the operation, and the inputs precisely:

> "On the **simplified, UTM-projected, LCC** primal graph of \<city\>, compute
> \<which centrality\>, **weighted by edge length**. Then \<the specific edge
> operation\>, recompute, and return the streets whose centrality changed most."

Notice what it does *not* say: it doesn't say "find the important streets." The
precision is the point. If your prompt is vaguer than this, the agent will
guess, and you'll spend INTERPRET time untangling its guess instead of reading
your result.

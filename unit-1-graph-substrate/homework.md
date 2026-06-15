# Unit 1 — Homework: From "Which Streets" to "How Fragile"

**Solo and asynchronous. Budget 60–90 minutes.**
**Same city, same stack, a new question.** Builds directly on the supervised
practice task — if you haven't done that, do it first.

> In class you found *which* streets pick up the load when one light-rail route
> removes some streets. The city now has a follow-up: **how fragile is our
> network to this kind of intervention in general?** Not "what happens if we
> build *this* line," but "what does it tell us that removing *these* streets
> hurts this much?"

You will go one step deeper and less scaffolded than the in-class task. Use the
same OSMnx v2 + pyrosm + igraph + folium stack from the demo — **no new heavy
dependencies**.

---

## Your task

Pick **one** of the two tracks below. Both are open-ended; both must run the
direct → interpret → extend loop and produce a filled decision log plus a short
writeup.

### Track 1 — Rank the candidates (extends baseline + extension (a))

Generate **three or four** plausible light-rail routes through your city (you
choose them; vary them — a radial route, a cross-town route, a route through
the dense core). For each, run the before/after centrality analysis from class.
Then **rank the routes** by how disruptive they are, using a structural
criterion *you define and defend*. A route that removes a low-betweenness
street but forces a big jump onto a single replacement street may be *more*
disruptive than one that removes a high-betweenness street with many parallel
alternatives — decide what "disruptive" should mean and let the data argue.

### Track 2 — Stress-test your own conclusion (extends extension (b) + (c))

Take the single route from your in-class baseline and pressure-test the
conclusion you defended:

1. **Metric sensitivity.** Re-run with **two** centralities you did not use in
   class. Does the set of "streets to worry about" stay stable, or does each
   metric nominate a different set? Quantify the overlap (how many of the
   top-10 streets are shared?).
2. **Wrong-class, concretely.** Identify **one specific street** in your result
   that you believe a topology-only analysis is *wrong* about — structurally
   central but realistically quiet, or structurally minor but actually jammed.
   Say exactly what you'd need to measure to confirm it, and which later unit of
   this course would give you that data.

---

## DIRECT / INTERPRET / EXTEND, on your own

You no longer have the instructor in the room, so the loop is entirely yours:

- **DIRECT** — prompts must use Unit 1 vocabulary (primal graph,
  simplification, projection/CRS, LCC, betweenness/closeness/degree, edge
  removal). Vague prompts cost you INTERPRET time later.
- **INTERPRET** — the homework is graded partly on whether you *noticed* and
  *chased* a surprise. If everything went exactly as you expected, look harder —
  or admit in writing that it didn't, and say why that itself is informative.
- **EXTEND** — your writeup must end on a question your results raised that you
  did **not** have time to answer. Name it precisely.

---

## Deliverables (push to your fork)

Push to `student-work/unit-1/` on your fork, then share the fork URL.

1. **Filled decision log** — one entry per direct → interpret → extend cycle
   (copy `decision-log-template.md`), with the end-of-session rubric check
   completed.
2. **A 300–500 word markdown writeup** that:
   - states the route(s) / metric(s) you chose and *why* (DIRECT + selection);
   - interprets your central result in **planning terms**, not just numbers
     (INTERPRET);
   - names at least one thing that surprised you, or argues honestly that
     nothing did and what that means;
   - ends on the unanswered follow-up question your results raised (EXTEND).
3. *(Optional but encouraged)* your working notebook or a couple of the folium
   maps, so a reader can see what you saw.

---

## A warning worth heeding

The most common way to lose points here is to report a high-betweenness street
as "where the traffic will go" without acknowledging that **betweenness is a
structural prediction, not measured flow.** It is fine — expected, even — to use
betweenness as your working hypothesis. It is *not* fine to forget that you did.
The one sentence of honesty about that limit is what separates a good writeup
from an excellent one.

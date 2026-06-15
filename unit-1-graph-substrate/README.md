# Unit 1 — The Graph Substrate

**Capability after this unit:** build a city road network from
OpenStreetMap; compute and interpret topological metrics (centrality,
meshedness); and justify a *graph + metric* pair against a real planner's
question — the foundational substrate the rest of the course builds on.

**Motivating question:** *Looking only at the road map, which streets are the
arteries — and how do we define "artery" rigorously enough for a computer to
find them?* The answer depends on two choices the analyst (and their AI) make:
**which centrality** defines "important," and **which graph** (intersections-as-
nodes vs. streets-as-nodes) you measure on. The unit's thesis: *there is no
neutral graph.*

## Where this sits in the course

Unit 1 establishes the vocabulary and the modeling-as-decisions mindset
(node/edge choices, projection, simplification, the centrality family, primal
vs. dual). Later units build on this substrate: trajectory mining (Unit 2),
statistical baselines (Unit 3), dynamic navigation (Unit 4), and graph neural
networks (Unit 5). The "betweenness ≠ realized traffic flow" caveat planted
here is paid off with real sensor flow in Unit 3 and time-varying weights in
Unit 4.

If you are new to the course, read [`../README.md`](../README.md),
[`../SETUP.md`](../SETUP.md), and the shared [`../rubric.md`](../rubric.md) +
[`../decision-log-template.md`](../decision-log-template.md) first.

## What's in this unit

| File | What it is |
|---|---|
| [`theory.md`](./theory.md) / `theory.pdf` / `theory.html` | The 45-min Marp slide deck. Citations are external DOI/arXiv links. |
| [`geoai-graph-unit1.ipynb`](./geoai-graph-unit1.ipynb) | The 45-min demo (Colab-first; local on macOS + Windows). Builds Jerusalem, computes three centralities, and contrasts the primal vs. dual graph on interactive maps. |
| [`practice-task.md`](./practice-task.md) | The 1-hour supervised-practice task (the light-rail stress test) you tackle with your agent. |
| [`homework.md`](./homework.md) | The take-home extension. |
| [`geoai-graph-unit1-solution.ipynb`](./geoai-graph-unit1-solution.ipynb) | The **reference solution** notebook — shows *a* strong path (not an answer key). See its top-cell disclaimer. |
| [`datasets.md`](./datasets.md) | Every data source + exactly how to access it (Geofabrik + pyrosm, bounding boxes, Drive fallback), locally with `uv` and on Colab. |
| [`further-reading.md`](./further-reading.md) | AI-friendly annotated source list (THEORY / PRACTICE / DATA / RECENT). Point your agent here for the concepts. |
| [`KNOWN_ISSUES.md`](./KNOWN_ISSUES.md) | Running list of install / runtime gotchas for this unit's stack. |
| [`student-work/`](./student-work/) | Your conflict-free workspace — never touched by the upstream. |

## How to run

- **Local (`uv`):** `uv sync --extra unit-1`, then open the notebooks with that
  environment's kernel. See [`../SETUP.md`](../SETUP.md).
- **Colab:** open the demo's Colab badge; the first cell runs `setup_colab.py`,
  which installs the unit's published `requirements/unit-1.txt`. Nothing to
  pre-install.

**Stack:** OSMnx v2, NetworkX, GeoPandas, Shapely, pyrosm, igraph, folium,
mapclassify, requests, gdown.

## Rights & disclaimer

© 2026 Ben Galon. All rights reserved. Part of the Geo-AI course (The Arena).
These materials are AI-assisted and instructor-reviewed — learning references,
not guaranteed-correct keys. See [`../NOTICE.md`](../NOTICE.md).

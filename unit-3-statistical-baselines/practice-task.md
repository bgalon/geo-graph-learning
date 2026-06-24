# Unit 3 — Supervised Practice: Cut a Corridor Into Segments, Then Forecast Each One

**Time: 1 hour, in class, working WITH an AI agent.**
**You will rehearse the loop: DIRECT → INTERPRET → EXTEND.**

> In Unit 2 you turned raw bus pings into **matched trajectories** on the road
> graph. In Unit 3's demo you took *one* sensor's speed series and asked **how
> far ahead can SARIMA beat a dumb floor** — the breakeven horizon. Now you
> **join the two skills**: take the whole Tel-Aviv ping pool, **map-match it
> onto a small corridor's road segments**, build a **per-segment speed series**
> from the pings themselves, and run the demo's breakeven workflow on **each of
> ~10 segments**.
>
> The headline question is no longer "is this one series predictable?" It is:
> **which segments of a real road are predictable, and why? Where does the
> breakeven horizon collapse — and what is it about that piece of road that
> breaks the forecast?**
>
> Your first and most important decision is one nobody hands you: **how do you
> cut the corridor into segments?** Per OSM edge? Fixed-length chunks?
> Junction-to-junction? That choice changes everything downstream — how dense
> each series is, how interpretable a "slow segment" is, whether SARIMA even has
> enough data to fit. Designing and *defending* that segmentation is the
> graded heart of this task.

This is **open-ended on purpose.** There is no single correct segmentation, no
single correct speed-filter, no single correct corridor. Two students who cut
the corridor differently can both produce defensible work. You are graded on
the **quality of your direct → interpret → extend loop** (see `rubric.md`), not
on matching a key or maximizing an R². The rubric rewards prompts in precise
unit vocabulary, interpretation in transit terms, and a follow-up you actually
chase — not the prettiest forecast.

---

## What you start from

Everything you need is in **this unit's** environment — **no new heavy
dependencies** (the geometry libs are light wheels, already in the `unit-3`
extra; there is **no separate Unit 2 install**):

- **Light geometry — `shapely` + `pyproj`:** the **EPSG:2039** projection
  transformers (`_tf` forward, `inv` inverse) so every distance is in **metres**,
  and **nearest-segment snapping** of pings onto a corridor via shapely's
  `STRtree` (`from shapely.strtree import STRtree` — built into shapely 2.x, no
  `rtree` needed). The reference builds the corridor by **following one bus
  line's shape** (its GPS centerline, recovered from its own GPS and buffered to
  a thin **±10 m ribbon**), then snaps pings to the nearest segment. This is the
  whole geometry stack — **no osmnx, no geopandas, no OSM road-graph fetch.**
  (If you genuinely want edge-based segments you may bring your own road graph,
  but it is *not* required and not part of the unit's deps — the line-shape
  ribbon is the sanctioned path.)
- **From the Unit 3 demo:** the **config cell** (`AGG`, `SEASON_M`, `HORIZONS`),
  the **ADF / ACF / PACF** stationarity check, the **one explained SARIMAX**
  fit, the fast fixed-order `statsforecast` `ARIMA(1,1,1)(1,1,1)_m` +
  `cross_validation(input_size=...)` walk-forward, the **historical-average and
  seasonal-naive floors**, the **breakeven horizon** logic, and the 80/95% fan
  chart.

The reference solution (`geoai-graph-unit3-solution.ipynb`) wraps the heavy
mechanics — snapping, speed-from-pairs, the per-segment forecast — into
**callable helper functions** (`line_centerline`, `cut_segments`,
`attribute_segment`, `pair_speeds`, `segment_series`, `fit_breakeven`, …).

> **What is sanctioned vs. what is not.** Importing or copying these **named
> helper functions** from the reference notebook is **encouraged** — the plumbing
> is *not* the graded work. You already did matching by hand in U2; here the
> graded work is the **decisions**: which corridor, how you cut it into segments,
> your speed filters and dwell rule, and your interpretation of which segments
> forecast well and why. What is **not** OK is copying the reference's *answers* —
> its corridor choice, its segmentation, its conclusions — and presenting them as
> yours. Reuse the helpers; make the calls yourself; own every parameter and
> defend it in your log.

You are **not** given the prompts to type. Composing the right request, in this
unit's vocabulary, is half the exercise.

---

## Your data — all of Tel Aviv

Fetch `tlv_all.parquet` exactly as the reference solution's data cell does — via
`gdown` with the id `1BqGMOa5urESNf-X3FHlMXZiFwIDp4EqQ` (~48 MB). It is the
**same file** you used in the Unit 2 practice. The exact id/URL and the
local-`uv`-vs-Colab access notes live in this unit's
[`datasets.md`](./datasets.md) — read it before you start so you are not
guessing the fetch.

`tlv_all.parquet` — **4.7 M pings**, 1458 lines, 6612 vehicles, **17 days**
(Feb 2023), over the TLV bbox **lat 32.00–32.15, lon 34.74–34.88**.
`recorded_at_time` is tz-aware UTC. The columns you need: `recorded_at_time`,
`lon`, `lat`, `bearing`, `velocity`, `line_ref`, `vehicle_ref`.

> **Filter to your corridor's bbox FIRST.** 4.7 M pings is a lot; clipping to a
> ~1–2 km corridor box drops it to a few thousand before you snap anything.
> Pick the corridor, cut to it, *then* map-match. (This is also why pooling
> **all** lines through the corridor matters — see below.)

> **Use the pings to compute speed — not the `velocity` column.** Your
> per-segment speed comes from **consecutive ping pairs of the same vehicle**
> (distance ÷ Δt in metres). The raw `velocity` column is an instantaneous
> snapshot; keep it only as an optional cross-check. (`velocity == 0` means
> *stopped at a light / stop dwell*, **not** missing — decide explicitly whether
> dwell belongs in your speed series.)

---

## The loop, made concrete

Everyone does the **baseline**. Then pick **at least one** extension (a/b/c/d);
strong students do two. Keep a **decision-log entry per cycle** (copy
`decision-log-template.md` into your working folder). In the in-class hour you
need only go deep on **2–3 segments** by hand; the reference solution runs all
~10 so you can compare.

### Baseline — every student

1. **Pick a small corridor and DESIGN its segmentation.** Choose a ~1–2 km
   stretch of a real TLV road that buses use heavily (a corridor with many
   lines through it gives dense series — that is the whole point of using
   all-TLV). Then **decide how to cut it into ~10 segments** and **write down
   why** in your log. Your options, each with a real trade-off:
   - **line-shape ribbon** (the reference) — follow one busy line's GPS
     centerline and keep a thin **±10 m ribbon**, cut into equal pieces. The
     corridor is a real road and the ribbon is unambiguous, but ±10 m is tight,
     so you lean on **pooling all lines** for density.
   - **per-OSM-edge** — segments = the road graph's own edges. Interpretable
     ("this edge is the block before the junction"), but edge lengths vary
     wildly, so series density varies segment to segment.
   - **fixed-length chunks** (e.g. ~150 m) — uniform density, but a chunk can
     straddle a junction and mix two regimes.
   - **junction-to-junction** — each segment is one block between intersections;
     the most physically meaningful, but you must detect junctions (graph nodes
     of degree ≥ 3).
   This is a **DIRECT/INTERPRET decision, not a mechanical step** — name the
   strategy in your prompt, in graph/geo vocabulary, and justify it against your
   corridor.
2. **Match ALL pings to your segments.** Project the corridor pings to
   EPSG:2039 and snap each to its **nearest segment** (nearest-segment snapping
   on a thin ribbon — or nearest road-graph edge if you went OSM-based — is fine
   for ~10 segments; full HMM map matching is the rigorous option, mention when
   you'd need it), and attribute each to the segment it falls on. Report **pings
   per segment** and **distinct vehicles per segment**.
3. **Compute per-segment speed from consecutive ping pairs.** For each vehicle,
   sort pings by time; for each consecutive pair on the **same segment**,
   `speed = distance(ping_i, ping_{i+1}) / Δt` in metres. Apply filters —
   **same `vehicle_ref`**, **sane Δt (~30–120 s)**, **drop zero-distance and
   teleport outliers** (state your speed ceiling). **Pool all lines/vehicles**
   through the segment into one 15-min-binned series. State your
   **minimum-passes-per-bin** rule — too few passes and SARIMA chases noise.
4. **Forecast each segment's speed (the demo's workflow, per segment).** For
   each of 2–3 chosen segments: ADF stationarity check, the seasonal difference
   at the daily lag, the fixed-order SARIMA, the **historical-average
   (weekday/weekend × time-of-day) and seasonal-naive floors**, **walk-forward**
   at 15/30/60 min, and the **breakeven horizon**. Show the error-vs-horizon
   plot with breakeven marked, and a fan chart for one segment.
   - **dow×tod is data-thin:** 17 days gives only ~2–3 samples per
     (weekday, time-of-day) cell, per segment. **Collapse to weekday vs weekend
     (Israeli weekend = Fri/Sat)** for the historical-average floor. The daily
     SARIMA season (`SEASON_M=96` @15min) is estimable; a weekly season is not.
5. **Read the segments back, in domain terms.** Compare your 2–3 segments:
   - **Which segment has the longest breakeven**, and what about it makes its
     speed predictable (a free-flowing block? a consistent rush-hour dip)?
   - **Which has the shortest / undefined breakeven**, and why (a junction
     approach where speed is dominated by signal timing? a segment so sparse
     SARIMA never beats the floor?).
   - For at least **one** segment, say whether the limitation is **the road**
     (genuinely erratic), **the data** (too few passes), or **your
     segmentation** (a chunk that mixed a junction with a free block).
6. **Defend your segmentation in one paragraph.** Given what you found, was your
   cut a good one? What would you change — and what could a transit planner
   trust your per-segment forecasts for, and for how far ahead?

### DIRECT / INTERPRET / EXTEND inside the baseline

- **DIRECT** — every request should name the operation in unit vocabulary:
  *corridor bbox clip, nearest-edge snapping, segment attribution, consecutive
  ping-pair speed, Δt filter, teleport outlier, minimum passes per bin, 15-min
  aggregation, ADF / stationarity, seasonal differencing, SARIMA order
  (p,d,q)(P,D,Q)_m, historical-average floor, seasonal-naive floor, walk-forward
  cross-validation, breakeven horizon, prediction interval*. If your prompt
  would read the same to a non-specialist ("predict the bus speed"), tighten it.
  **And: name your segmentation strategy explicitly** — "split by OSM edge" vs
  "150 m fixed chunks" is a DIRECT decision the agent must not make for you.
- **INTERPRET** — when the agent returns a breakeven number, a series, or a map,
  restate it: *how far ahead* the segment is predictable, *where* the floor
  wins, and whether that matches your intuition about that piece of road. A
  breakeven that surprises you is a lead, not a bug to hide.
- **EXTEND** — your per-segment results should raise a new question. Follow it.
  The extensions below are structured leads, but a good question of your own
  counts.

---

## Extensions (pick at least one)

### (a) Upstream → downstream lead — *the U5 seed* — *the surprise*

Order your segments along the direction of travel. For an **adjacent pair**,
compute the **lagged cross-correlation** between the upstream segment's speed at
time *t−k* and the downstream segment's speed at *t*. Does congestion
**propagate** — does the upstream slowdown *lead* the downstream one by a few
bins? Plot corr vs lag; report the lead time. Then ask: **if you added the
upstream segment's recent speed as an input, would the downstream breakeven
extend?** (You don't have to build the multivariate model — articulate the
hypothesis precisely. This is exactly the spatial signal U5's message-passing
graph nets exploit.) Most students get a genuine "the slow patch *moves
upstream*" moment.

### (b) Segmentation-strategy A/B

Re-cut the **same corridor** a second way (e.g. per-OSM-edge vs ~150 m fixed
chunks) and re-run the per-segment breakevens. **Does the segmentation change
which segments look predictable?** Plot breakeven-by-segment for both cuttings
and explain the difference in domain terms: fixed chunks that straddle a
junction blur a real signal; per-edge segments isolate it but starve the short
ones of data. Which cut would you ship, and why?

### (c) Dwell in or out — the `velocity == 0` decision

Build the per-segment speed series **two ways**: once **including** stopped
pings (dwell counts as low speed) and once **excluding** them (rolling speed
only). Compare the two series' distributions, their ADF results, and their
breakevens. **Does removing dwell make the segment more predictable or just
hide the congestion you care about?** Tie it back to the demo's METR-LA "0 =
missing" contrast — here 0 means *stopped*, a real state.

### (d) Wrong-class — when does SARIMA stop being the right tool? *(meta)*

You forecast each segment **independently** and **univariately**. Articulate, in
domain terms, the conditions under which that is the wrong choice: when a
segment is too sparse for *any* univariate model (the floor wins at every
horizon → you need pooling or a spatial model); when the Feb-2023 window
straddles an **anomaly** (weather / strike) that no daily-seasonal model can
see; and when the **spatial** signal from extension (a) means a *graph* model
(U5) would beat ten independent SARIMAs. Name what later units supply to fix
each.

---

## How the hour runs

| Time | What you do |
|---|---|
| 0:00–0:05 | Instructor restates the task + the rubric; you confirm your corridor + segmentation strategy + speed filters. |
| 0:05–0:45 | Work the loop WITH the agent. Fill a decision-log entry per cycle. Go deep on 2–3 segments. |
| 0:45–0:55 | 2–3 students share a **surprising follow-up** they hit (the segment with no breakeven, the upstream lead, the segmentation flip). |
| 0:55–1:00 | Instructor synthesis. |

---

## What you hand in

- Your **decision log** (one entry per direct → interpret → extend cycle), with
  the end-of-session rubric check filled in. Your **segmentation strategy + the
  reason for it** is a required log entry.
- Your **per-segment breakeven comparison** (a small table or plot: segment →
  breakeven horizon) and your **one-paragraph segmentation defence**.
- The extension(s) you chose, captured in the log.

You do **not** need a polished notebook for the in-class hour — the log + the
comparison + your maps are the deliverable. (The take-home `homework.md` asks
for a short writeup.)

---

## A note on prompting (example *structure*, not a script)

You compose your own prompts. As a shape to imitate — not copy — a good DIRECT
request names the object, the operation, and the inputs precisely:

> "Build the corridor by following line \<line_ref\>'s shape (its GPS
> centerline, ±10 m ribbon), project to **EPSG:2039**, and **snap each ping to
> its nearest segment**. Cut the corridor into segments **by \<strategy:
> ±10 m line-shape / per-OSM-edge / 150 m fixed chunks / junction-to-junction\>**
> — I chose this because \<reason\>. For each segment,
> compute speed from **consecutive same-vehicle ping pairs** (Δt in 30–120 s,
> drop teleports above \<ceiling\> km/h), **pool all lines**, and bin to 15 min
> keeping only bins with ≥ \<k\> passes. Then run the breakeven workflow per
> segment: ADF, fixed-order SARIMA `(1,1,1)(1,1,1)_96`, vs the
> **weekday/weekend × time-of-day historical-average** and seasonal-naive
> floors, walk-forward at 15/30/60 min."

Notice what it does *not* say: it doesn't say "predict the bus speed and check
if it's good," and it doesn't let the agent pick the segmentation or the speed
filters. The precision is the point. If your prompt is vaguer than this, the
agent will choose your segmentation (and your outlier rule) for you — and you'll
spend INTERPRET time reverse-engineering its choices instead of owning them.

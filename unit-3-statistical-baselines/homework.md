# Unit 3 — Homework: From per-segment speed to a corridor *travel-time budget*

> **Builds on the supervised task.** Same data (all-TLV `tlv_all.parquet`, Feb
> 2023), same corridor, a new question. Solo and asynchronous. Budget **60–90
> minutes**. In class you forecast **per-segment speed**; at home you turn those
> segments into a **corridor-level travel-time budget** and ask whether the
> *whole-corridor* forecast is more or less predictable than its parts.

## Why this question

In class you treated each segment in isolation and asked which were predictable.
Operationally, a rider or a dispatcher does not care about one block — they care
about **how long the whole corridor takes to drive, and when**. That whole-
corridor traversal time is the **sum of the segment crossing-times**, and it has
different statistics from any single segment: the noisy short segments partly
**average out**, but a single chronically-jammed junction segment can
**dominate** the budget. The point of this homework is to feel how aggregation
across segments changes predictability — and to say so precisely, in the
breakeven vocabulary.

## The task

Reuse your in-class corridor and its ~10 segments (or re-cut it — your choice,
just state it and why).

1. **Build a per-segment crossing-time series.** For each segment, convert its
   15-min mean speed into an **expected crossing time** for that segment
   (`segment_length / mean_speed`, in seconds), on the same 15-min cadence you
   used in class. Handle empty bins explicitly (interpolate? carry forward?
   drop? — state your rule and why; this is the EXTEND decision).
2. **Sum to a corridor travel-time budget.** For each 15-min bin, sum the
   segment crossing-times into a **whole-corridor travel-time series** (seconds
   to drive the corridor end-to-end). Plot it; shade weekends (Fri/Sat). Run
   **ADF** on it.
3. **Forecast the corridor budget.** Fit SARIMA + the **weekday/weekend ×
   time-of-day historical-average** and **seasonal-naive** floors,
   **walk-forward** at 15/30/60 min, and find the **breakeven horizon for the
   corridor travel-time budget.**
4. **Compare to the parts.** Put the corridor breakeven next to your in-class
   **per-segment** breakevens. Is the aggregated budget **easier** or **harder**
   to forecast than the individual segments? Argue from the statistics — does
   summing **average out** segment noise (longer breakeven), or does **one
   dominant jammed segment** carry the whole budget (the corridor inherits the
   worst segment's short breakeven)? Identify which segment dominates the budget
   variance.

## Deliverables (push to your fork)

Push to `unit-3-statistical-baselines/student-work/` in your fork, then share
the **fork URL**.

1. **A filled decision log** (`decision-log-template.md`) — your prompts, your
   empty-bin rule, the corridor breakeven, and the per-segment breakevens you
   are comparing against.
2. **A 300–500-word markdown writeup** (`writeup.md`) that **interprets** your
   results in transit terms. It must answer:
   - What was your corridor + segmentation + empty-bin rule, and why?
   - Was the whole-corridor travel-time budget **easier or harder** to forecast
     than its segments, and what in the *statistics* (not your gut) made it so?
   - Which segment **dominates** the corridor budget's variance, and what does
     that say about where a transit agency should invest (signal retiming? a bus
     lane)?
   - One thing that surprised you and a follow-up question it raises.
3. (Optional) your notebook or a couple of figures.

## Grading

Applied against `rubric.md` (DIRECT / INTERPRET / EXTEND) with the
unit-specific notes your instructor keeps. The **writeup carries the INTERPRET
weight** — a clean breakeven number with a hand-wavy explanation scores below a
messier result with a precise, statistics-grounded argument about
averaging-vs-domination.

> **Hint, not a spec:** the answer to "easier or harder" is *not* automatic.
> Summing independent-ish segments tends to **smooth** noise (central-limit
> intuition → longer breakeven), but if one junction segment's variance swamps
> the rest, the corridor budget tracks *that* segment and inherits its short
> breakeven. Your empty-bin rule matters too: a careless carry-forward can
> inject a fake daily cycle that makes the budget *look* more predictable than
> it is. Show the distributions and the per-segment variance that justify your
> claim.

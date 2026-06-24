# Unit 3 — Statistical Baselines

**Capability after this unit:** define and evaluate a univariate forecasting
**baseline** on a real speed series, and use it as the **spec for "better."** You
fit a seasonal ARIMA in the open (Box–Jenkins: stationarity → ACF/PACF →
differencing → fit → residual diagnostics), run an honest **walk-forward**
evaluation, and find the **breakeven horizon** at which the baseline degrades to
a simple historical-average floor. You finish able to **choose a baseline class
by the question**, read a forecast in domain terms, and name the **spatial gap**
(a sensor cannot see its upstream neighbour) that motivates the graph model in
Unit 5.

This unit runs on **METR-LA** (LA freeway loop-detector speeds — the
already-Eulerian, fixed-sensor regime) for the demo, and on the **Tel Aviv bus
archive** (`tlv_all.parquet`, the per-vehicle GPS regime turned into per-segment
series) for the practice.

> **Numbering note.** Statistical Baselines is **Unit 3** in our teach order.
> The original syllabus PDF labels it Unit 4. Every public-side artifact uses
> the teach-order numbering.

---

## What's here

| File | What it is |
|---|---|
| [`theory.pdf`](./theory.pdf) / [`theory.html`](./theory.html) | The 52-slide theory deck (45 min). Citations are external DOI/arXiv links. |
| [`geoai-graph-unit3.ipynb`](./geoai-graph-unit3.ipynb) | **Demo** — one METR-LA freeway sensor: load → see daily/weekly seasonality → ADF + ACF/PACF + differencing → one transparent SARIMAX (+ Kalman as its online cousin) → walk-forward across 15/30/60-min horizons → the **breakeven horizon** → an upstream sensor's lagged cross-correlation (the spatial gap, the bridge to Unit 5). Colab-first; smoke-test cell up top. |
| [`practice-task.md`](./practice-task.md) | **Supervised practice** — take one bus line's shape as a thin corridor, design a segmentation strategy (~10 road segments), build a per-segment speed series from consecutive ping pairs, and find each segment's breakeven against strong floors. |
| [`homework.md`](./homework.md) | The take-home extension (corridor travel-time budget = Σ segment crossing-times). |
| [`geoai-graph-unit3-solution.ipynb`](./geoai-graph-unit3-solution.ipynb) | **Reference solution** — *a* complete, runnable path through the practice (not an answer key; the task is open-ended). Carries an AI-assisted disclaimer. |
| [`datasets.md`](./datasets.md) | Every data source + exact IDs/bbox, and how to access them **locally (`uv`)** and **on Colab**. |
| [`further-reading.md`](./further-reading.md) | AI-friendly sources page — every paper + tool as an external link + a short summary, grouped Foundations / Traffic baselines / METR-LA bridge / Transit / Datasets. |
| [`references.bib`](./references.bib) | The unit's BibTeX (machine-readable citations pairing with `further-reading.md`). |
| [`KNOWN_ISSUES.md`](./KNOWN_ISSUES.md) | "If you see X, do Y" — the fragile bits (METR-LA `0`-means-missing, `h5py` vs `pd.read_hdf`, SARIMA walk-forward timing, UTC→`Asia/Jerusalem`). |

## How to run

- **Local (`uv`):** `uv sync --extra unit-3`, then open the notebook with the
  `geo-graph` kernel. See [`../SETUP.md`](../SETUP.md). The `unit-3` extra
  installs the forecasting stack (statsmodels, statsforecast, h5py, folium,
  gdown, pyarrow) plus the light geometry libs (shapely, pyproj) the practice
  needs.
- **Colab:** click the badge at the top of the demo notebook; the first cell
  installs the unit's published dependencies. Nothing to pre-stage — each
  notebook fetches and subsets its own data inline.

See [`datasets.md`](./datasets.md) for data access and
[`further-reading.md`](./further-reading.md) for the concepts (both written so
your agent can use them as context).

## Where this sits in the course

- **Unit 2** produced the matched trajectories this unit aggregates — the
  **Lagrangian → Eulerian** shift: per-vehicle pings become per-segment speed
  time series.
- **This unit** builds the **strong baseline** every later model must beat, and
  measures where a single-series forecast runs out of signal.
- **Unit 4** reuses the per-segment speed series as **time-varying edge weights**
  (the peak-vs-off-peak finding is a direct seed).
- **Unit 5** is the literal target: the breakeven, the upstream→downstream lead,
  and the one-segment residual are exactly what a graph model must improve by
  exploiting the neighbour signal you measured here.

---

Rights & disclaimer: see [`../NOTICE.md`](../NOTICE.md). Materials are
AI-assisted and instructor-reviewed — verify before you rely on them. Your work
goes in [`student-work/`](./student-work/).

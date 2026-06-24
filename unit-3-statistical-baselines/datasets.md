# Unit 3 — Data sources & how to access them

This unit's **demo** runs on **METR-LA** (LA freeway loop-detector speeds — the
already-Eulerian, fixed-sensor regime); the **supervised practice + reference
solution** run on **`tlv_all.parquet`**, the all-Tel-Aviv bus-GPS slice (the
Lagrangian per-vehicle regime you turn into per-segment series). Every notebook
fetches and subsets its own data **inline**, so it runs end-to-end on a fresh
Colab with nothing pre-staged. This page lists every source, the exact IDs/URLs,
and how access differs locally (`uv`) vs. on Colab.

> **Attribution (required).**
> - **METR-LA:** Li, Yu, Shahabi & Liu, *DCRNN* (ICLR 2018) — the LA Metro loop
>   detector speeds. See [`further-reading.md`](./further-reading.md) → "METR-LA
>   / spatio-temporal bridge". Keep this attribution on any figure you publish.
> - **Bus GPS:** Israel Ministry of Transport SIRI feed, archived by **The
>   Public Knowledge Workshop (HaSadna)** via the *Open Bus* project — see
>   [`further-reading.md`](./further-reading.md) → "Datasets / tooling".

---

## 1. METR-LA — the demo's freeway-detector speeds

The demo cuts **two sensor columns** out of the full METR-LA HDF5 in-cell, so
nothing is hand-staged. Source data is `[34272, 207]` (5-min cadence × 207
detectors). The two pinned sensors are a freeway-mainline target (`773012`) and a
physically-upstream neighbour (`760650`, ~10-min lead).

| Path | Source | Size | Notes |
|---|---|---|---|
| **Primary** | `metr-la.h5` on a public GitHub raw mirror | ~57 MB | CDN-backed, no per-file rate limit; the demo reads it with `h5py` and cuts the 2 columns |
| **Fallback** | curated 2-column parquet on Google Drive | tiny | optional fast backup; the `METR_LA_DRIVE_ID` slot is wired after upload |

```python
import urllib.request, h5py, pandas as pd
URL = "https://raw.githubusercontent.com/deepkashiwa20/MegaCRN/main/METRLA/metr-la.h5"
urllib.request.urlretrieve(URL, "metr-la.h5")
# the demo reads /df/axis0 (columns), /df/axis1 (index), /df/block0_values via h5py
```

- **The `0` gotcha:** in raw METR-LA, **`0` mph means "sensor missing", not
  "stopped traffic"** — the demo replaces `0.0 -> NaN` before any stationarity
  diagnostic. (Contrast with the bus data below, where `velocity == 0` is a real
  *stopped* state — see §2.)
- **Why `h5py`, not `pd.read_hdf`:** sidesteps pandas/pytables version fragility
  (`h5py` is pre-installed on Colab). See `KNOWN_ISSUES.md`.

## 2. `tlv_all.parquet` — the practice's all-TLV bus-GPS slice

The supervised practice + reference solution use **the same file as Unit 2**: a
pre-cut **zstd parquet** of every Tel Aviv bus ping. `gdown` it once; read with
pandas/pyarrow.

| Used by | File | Drive id | Size | Contents |
|---|---|---|---|---|
| **Practice / solution** | `tlv_all.parquet` | `1BqGMOa5urESNf-X3FHlMXZiFwIDp4EqQ` | ~48 MB | **All** Tel Aviv pings: ~4.7 M rows, 1,458 lines, 6,612 vehicles, 17 days (Feb 2023) |

```python
import gdown, pandas as pd
gdown.download(id="1BqGMOa5urESNf-X3FHlMXZiFwIDp4EqQ", output="tlv_all.parquet", quiet=False)
df = pd.read_parquet("tlv_all.parquet")          # ~4.7M pings over the TLV bbox
```

- **Columns (7):** `recorded_at_time` (tz-aware **UTC**), `lat`, `lon`,
  `bearing`, `velocity`, `line_ref`, `vehicle_ref`.
- **Tel Aviv bounding box** (WGS84): **lat 32.00–32.15, lon 34.74–34.88**.
- **Cadence** ≈ 1 GPS fix per vehicle per minute (the sparse regime).
- **`velocity == 0` means *stopped*** (light / stop dwell), **not missing** — the
  opposite of METR-LA. Decide explicitly whether dwell belongs in your
  per-segment speed series (practice extension (c)).
- **Speed comes from ping *pairs*, not the `velocity` column:** for consecutive
  same-vehicle pings, `speed = distance / Δt` after projecting to **EPSG:2039**
  (so distances are in metres). The `velocity` column is only an optional
  cross-check.

## 3. Provenance — the raw SIRI archive (NOT on the runtime path)

The canonical source `tlv_all.parquet` is derived from. You do **not** need it
to run anything; it is listed so the slice is reproducible, not hand-staged.

- **File:** `busarchive.bin` (1.22 GB ZIP), Drive id
  `1BniXRYr5DrYvY_miHpD-hjChFB8s1ac6`; the GPS lives in
  `exports/vehicle_locations.parquet` (Feb 2023). Regenerate a cut: download →
  extract that member → keep the 7 columns → filter to the TLV bbox → write zstd
  parquet. (See the solution notebook's inert "provenance" appendix cell.)

---

## Local vs. Colab — what differs

The **same notebook code runs in both places**; only where data is cached
differs.

| | Local (`uv`) | Colab |
|---|---|---|
| Setup | `uv sync --extra unit-3` | first cell runs `setup_colab.py` → `setup_unit("unit-3")` |
| Working dir / cache | your cwd | `/content` (resets each session) |
| METR-LA h5 | `urlretrieve` once, cached on disk | `urlretrieve` per fresh runtime |
| `tlv_all.parquet` | `gdown` once, cached on disk | `gdown` per fresh runtime |

The `unit-3` extra now also carries the **light geometry libs** (`shapely`,
`pyproj`) the practice's corridor needs — there is **no separate Unit 2
install**. Nearest-segment snapping uses `shapely.strtree.STRtree` (built into
shapely 2.x; no `rtree`). If you move the data cache, tell your agent the new
path explicitly.

## Gotchas (the ones that bite)

- **`velocity == 0` flips meaning between the two datasets:** METR-LA `0` =
  *missing* (mask to NaN); bus GPS `0` = *stopped* (real signal). Carrying the
  METR-LA habit into the bus data silently deletes the congestion you want.
- **`recorded_at_time` is UTC.** Convert to `Asia/Jerusalem` before any local-
  time window (rush-hour slice, weekday/weekend split — Israeli weekend = Fri/Sat).
- **Clip to your corridor's bbox FIRST.** 4.7 M pings is a lot; clipping to a
  ~1–2 km corridor box drops it to a few thousand before you snap anything.
- **Project to EPSG:2039 before any metres-based step.** Speeds, Δt distance
  filters, and segment lengths are all in metres; computing them on lat/lon
  degrees is silently wrong.

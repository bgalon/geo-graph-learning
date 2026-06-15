# Unit 1 — Known Issues

If you hit an install or runtime issue, check this file first. Format:

```
## <short symptom>
**Symptom:** What you see (error message, unexpected output).
**Cause:** Best understanding of why it happens.
**Fix:** Concrete steps to recover.
```

---

## OSMnx v1 vs v2 API

**Symptom:** Smoke-test cell raises `AssertionError: This demo requires
osmnx>=2.0`, or later cells fail with `AttributeError: module 'osmnx' has no
attribute 'simplification'` / `'projection'` / `'convert'` / `'io'`.
**Cause:** The notebook is written against the **OSMnx v2.x** module layout
(`ox.simplification.*`, `ox.projection.*`, `ox.convert.*`, `ox.io.*`). A v1.x
install exposes the old flat API (`ox.simplify_graph`, `ox.project_graph`,
`ox.graph_to_gdfs`, `ox.save_graphml`) and the 2017 helpers.
**Fix:** `pip install -U "osmnx>=2.0,<3.0"` and restart the runtime. On Colab the
setup cell pins this; if you installed osmnx yourself first, the older version
may win — uninstall it (`pip uninstall -y osmnx`) and re-run the setup cell.

## Colab smoke test fails after setup: numpy `_center` / ABI errors

**Symptom:** The setup cell installs many packages, then the smoke test (or any
geo import) raises e.g. `cannot import name '_center' from 'numpy._core.umath'`
(or similar numpy/pandas ABI errors).
**Cause:** TWO things. (1) If `requirements/unit-1.txt` is the **full pinned
dependency tree** (it pins `numpy==…`, `pandas==…`), the setup cell
force-reinstalls Colab's core scientific stack — and numpy changing **mid-
session** leaves a half-loaded, inconsistent numpy. (2) On Colab, ANY change to
numpy/pandas/scipy requires a **runtime restart** before those libs import
cleanly.
**Fix:**
- Quick (any session): **Runtime → Restart session**, then re-run from the smoke
  test — do **NOT** re-run the setup cell. If it still fails, install floors-only
  in one cell and restart again:
  `!pip install -q "osmnx>=2.0,<3.0" networkx geopandas shapely requests pyrosm igraph folium mapclassify`
- Why this happens: `requirements/<unit>.txt` lists only the unit's **direct**
  deps with floors — NOT the full pinned tree — so Colab keeps its own
  numpy/pandas (avoids ABI breaks). A restart is normal after a core-lib bump.

## pyrosm install fails on Colab / Windows

**Symptom:** The setup or smoke-test cell errors on `import pyrosm`, or
`pip install pyrosm` fails building a wheel (Cython / pyrobuf compile errors,
or "no matching distribution" on a very new Python).
**Cause:** `pyrosm` is now a **student runtime dep** (the notebook cuts the
Geofabrik extract inline). Its wheels lag new Python releases and can be fragile
on Windows.
**Fix:**
- On Colab: re-run the setup cell (it pins a working pyrosm); if it still fails,
  `pip install -U pyrosm` and restart the runtime.
- On Windows: prefer conda-forge — `conda install -c conda-forge pyrosm`.
- **Fallback that needs NO pyrosm:** the notebook's Section 3b has an OPTIONAL
  hosted-GraphML path. Set `JERUSALEM_PRIMAL_FALLBACK_URL` (Section 3b) to a raw
  URL of a small `jerusalem_primal.graphml` (produce one with
  `make_overlay_asset.py --emit-graphml`). That path loads via `ox.io.load_graphml`
  and imports only OSMnx — no pyrosm required.

## Geofabrik download is slow / 504s / fails in class

**Symptom:** Section 3b sits at "downloading the Israel-and-Palestine Geofabrik
extract (~100-130 MB, once)…", or raises `504 Server Error: Gateway Timeout`
(or a connection/timeout error) for `download.geofabrik.de`.
**Cause:** The notebook downloads the regional `.osm.pbf` once per fresh runtime.
It's the single slowest, most failure-prone step; Geofabrik occasionally returns
a transient **504 Gateway Timeout** (server busy — not a block).
**Fix (mostly automatic now):**
- **Retries:** the download retries with exponential backoff (4 attempts). A
  transient 504 usually clears on a retry — just let it run, or re-run the cell.
- **Caching:** once `/content/israel-and-palestine.osm.pbf` exists, re-runs skip
  the download. Pre-warm the runtime before class by running Section 3b once.
- **Google Drive fallback (default):** if Geofabrik keeps failing, the cell
  auto-falls-back to a hosted Google Drive copy (`JERUSALEM_PRIMAL_DRIVE_ID`,
  downloaded via `gdown`). The file may be the `.pbf` OR a prebuilt
  `jerusalem_primal.graphml` — the cell sniffs the bytes and handles either
  (GraphML → `ox.io.load_graphml`; `.pbf` → pyrosm cut). To swap in your own
  Drive copy, replace the file id; ensure the Drive file is **share = Anyone
  with the link**.
- **Optional GraphML URL:** as a last resort, set `JERUSALEM_PRIMAL_FALLBACK_URL`
  to a raw `jerusalem_primal.graphml` URL.
- If **all** sources fail, the cell prints a clean one-line summary of each
  source's error (no IPython traceback noise) and stops.

## (resolved) Self-contained data — no placeholder URL anymore

The notebook used to load a pre-staged GraphML from a `<JERUSALEM_PRIMAL_RAW_URL>`
placeholder that a human had to fill in. **That is gone (rework 2026-06-12):**
Section 3b now downloads Geofabrik + cuts Jerusalem with pyrosm **inline**, so a
fresh Colab runs end-to-end with NO human staging. The only optional knob is
`JERUSALEM_PRIMAL_FALLBACK_URL` (default empty), a safety net — see the two
entries above. The `make_overlay_asset.py` script is slide/fallback-asset-only
and is NOT on the demo runtime path.

## Centrality looks wrong / distances are tiny

**Symptom:** Closeness/betweenness values are nonsensical, or edge `length`
values are ~0.001.
**Cause:** The graph is **unprojected** (CRS in degrees, EPSG:4326). Length-
weighted metrics then measure in degrees, not meters — silently wrong.
**Fix:** Confirm the "projected?" check in Section 3c prints `True`. Section 3b
projects the freshly-built graph to UTM via `ox.projection.project_graph`; if you
swapped in your own graph, run `G = ox.projection.project_graph(G)` first.

## GeoPandas / Shapely install on Windows

**Symptom:** `pip install geopandas` fails building Fiona/GDAL, or import errors
about GDAL DLLs on Windows.
**Cause:** Older toolchains needed compiled GDAL. Modern GeoPandas (>=1.0) +
Shapely (>=2.0) ship pure wheels, but a stale pip or Python version can still
miss them.
**Fix:** Upgrade pip (`python -m pip install -U pip`) then `uv sync --extra
unit-1` (or `pip install "geopandas>=1.0" "shapely>=2.0"`). If it still fails,
use conda-forge: `conda install -c conda-forge geopandas`. The student notebook
needs no GDAL-CLI — only geopandas/shapely (and `pyrosm`, which has its own entry
above; on Windows prefer conda-forge for pyrosm too).

## Betweenness/closeness is slow (now solved with igraph)

**Symptom:** On the few-thousand-node LCC, `nx.closeness_centrality` +
`nx.betweenness_centrality` (pure-Python) take ~20 minutes.
**Cause:** Both are O(V·E); pure-Python NetworkX does not scale.
**Fix (now baked in):** Section 4 computes closeness + betweenness with
**igraph** (C-backed) instead — identical exact values in **seconds**. `igraph`
is now a **unit-1 runtime dep** (in the smoke test + requirements). Degree stays
on NetworkX (instant). If you widened `JERUSALEM_BBOX` a lot and even igraph is
slow, sample (`g.betweenness(... )` on a subgraph) or tighten the bbox.

## igraph install / normalization

**Symptom:** Smoke-test errors on `import igraph`; or igraph centrality numbers
don't match NetworkX.
**Cause:** The PyPI package is named **`igraph`** (import `igraph` /
`import igraph as ig`) — *not* the legacy `python-igraph` import name. And
igraph returns **raw (unnormalized) betweenness**, while the demo uses
NetworkX-style **normalized** betweenness.
**Fix:**
- Install: `pip install igraph` (Colab + macOS + Windows all have wheels;
  no compiler needed). If an old `python-igraph` shadows it, `pip uninstall -y
  python-igraph` first.
- Normalization (already handled in Section 4): rescale igraph betweenness by
  `2/((n-1)(n-2))` for an undirected graph to match
  `nx.betweenness_centrality(..., normalized=True)`. igraph
  `closeness(normalized=True)` already matches NetworkX on a single connected
  component (the LCC), so closeness needs no rescale.

## folium maps don't render, or are in the wrong place (CRS gotcha)

**Symptom:** A folium map shows blank/grey, renders nothing inline, or the
network appears in the ocean off West Africa (lat/lon ≈ 0,0).
**Cause:** Two common causes. (1) On Colab, a folium `Map` only renders inline
if it is the **last expression** of the cell (or wrapped in `display(m)`).
(2) **The CRS gotcha:** the graph is projected to **UTM (meters)** for the
metrics, but folium/Leaflet needs **WGS84 lat/lon (EPSG:4326)**. Passing UTM
coordinates straight to folium puts everything at nonsense locations.
**Fix:**
- Render: end the cell with `m` (or `display(m)`); folium is in the smoke test.
- CRS: build node/edge GeoDataFrames and **`.to_crs(4326)` for rendering only**
  (Sections 5, 6, and the appendix do this). Do **NOT** recompute metrics on the
  unprojected graph — compute on UTM, reproject only the geometry to draw it.
- Basemaps: the demo uses OpenStreetMap, an Esri World Imagery `TileLayer`, and a
  **blank** background (a 1×1 transparent-PNG data-URI tile) so pure topology
  shows with no map underneath. The Esri tiles require network access; if a
  corporate proxy blocks `server.arcgisonline.com`, only that basemap is blank —
  switch to OpenStreetMap in the layer control.

## Live dual build runs long in class

**Symptom:** Section 6 `build_named_street_dual` / dual betweenness eats into the
45-min budget.
**Cause:** Unlikely on the Jerusalem cut (a few seconds), but possible on a
larger graph.
**Fix (instructor):** set `USE_FALLBACK = True` in the overlay cell and set
`OVERLAY_PNG_URL` to a hosted `jerusalem_dual_overlay.png` (produced by
`make_overlay_asset.py`) to display the pre-rendered figure and keep moving.

---

## Asset-script notes (instructor / `make_overlay_asset.py`, OFF the demo path)

**`make_overlay_asset.py` is NOT on the demo runtime path.** The notebook is
self-contained. This script only pre-renders OPTIONAL static assets: the
`jerusalem_dual_overlay.png` slide/fallback figure and, with `--emit-graphml`, an
OPTIONAL fallback `jerusalem_primal.graphml`. Neither is required to run the demo.
It needs an **open network** (Geofabrik downloads are blocked in restricted/CI
sandboxes — run it on Colab or a laptop). Note `pyrosm` is now ALSO a student
runtime dep (see the pyrosm entry above), not just an asset-script dep.

# Unit 3 — Known Issues (Statistical Baselines)

Per-unit install/runtime gotchas for `geoai-graph-unit3.ipynb` and
`geoai-graph-unit3-solution.ipynb`. Format: **if you see X, do Y.**

## Setup / dependencies

### If the setup cell prints `WARN/404` for `requirements/unit-3.txt`
Nothing unit-specific installed, so the smoke test fails at `import
statsforecast`. **Do:** confirm you are on a fresh runtime with network access
and re-run the first cell — it fetches `requirements/unit-3.txt` from the public
repo's `main` over HTTP. Locally, run `uv sync --extra unit-3` instead (the
setup cell is a no-op in a `uv` env).

### If `import statsforecast` / `import numba` fails on **Windows**
`statsforecast` depends on `numba`, which needs a matching LLVM-lite wheel.
Most recent Python versions have Windows wheels, but a brand-new Python release
can lag. **Do:** use Python 3.11/3.12 (not the newest pre-release); if a wheel
is still missing, run on Colab (the supported path) or in WSL. `statsmodels`,
`pandas`, `pyarrow`, `folium`, `shapely`, `pyproj` all have Windows wheels and
are unaffected.

### First `ARIMA` fit is slow / "hangs" for a few seconds
That is the one-time **numba JIT compile**, not a hang. The smoke-test cell
warms it deliberately so the timed walk-forward loop is fast.
**Do:** let the smoke-test cell finish; subsequent fits are fast.

## Data

### METR-LA: if the primary `metr-la.h5` fetch fails
The demo fetches the full `metr-la.h5` from a public GitHub-raw mirror and cuts
the two sensor columns in-cell. **Do:** if the mirror is unreachable, set
`METR_LA_DRIVE_ID` in the loader cell to the curated 2-column parquet on the
course Drive (the fallback). The fetch is cached; delete the cached file to force
a re-download. See [`datasets.md`](./datasets.md).

### Why `h5py` and not `pd.read_hdf`
The loader reads METR-LA with `h5py`, not `pd.read_hdf`, to sidestep
pandas/pytables version fragility. `h5py` is pre-installed on Colab and in the
`unit-3` extra.

### Zeros in METR-LA mean "missing", not "0 mph"
In raw METR-LA, **`0` mph means the sensor was missing**, not stopped traffic.
The notebook does a defensive `.replace(0, NaN)` before any ADF/ACF/differencing
and shows the missing-fraction check. **Do:** always mask zeros before any
stationarity diagnostic — otherwise the diagnostics lie. (Contrast the bus data
in the practice, where `velocity == 0` is a real *stopped* state — see
[`datasets.md`](./datasets.md).)

### Practice: `tlv_all.parquet` (the bus-GPS slice)
`gdown` the 48 MB cut (id in [`datasets.md`](./datasets.md)); read with pandas.
**Do:** project to **EPSG:2039** before any metres-based step (speed from ping
pairs, distance filters, segment lengths), and convert `recorded_at_time` from
**UTC** to `Asia/Jerusalem` before any local-time window (rush hour, the Israeli
Fri/Sat weekend split). Clip to your corridor bbox first to drop ~4.7 M pings to
a few thousand before snapping.

## Evaluation

### The walk-forward loop runs longer than ~5 min on Colab
**Do:** apply a pacing safety valve, in order: (1) keep the default 15-min
aggregation (`AGG="15min"`, `SEASON_M=96`); (2) lower `N_WINDOWS`; (3) drop
`SeasonalNaive` from the `cross_validation` models list (the breakeven only needs
SARIMA + HistoricAverage). The native 5-min config (`SEASON_M=288`) is heavier —
time it before using it in class.

### `MAPE` is `inf` / `NaN`
MAPE divides by actual speed and blows up near zero. **Do:** read RMSE/MAE as the
primary metrics; treat MAPE as indicative only. The scoring cell already guards
with `.replace(0, NaN)`.

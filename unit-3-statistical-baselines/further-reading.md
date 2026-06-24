# Unit 3 — Further reading (AI-friendly sources)

Every source behind the Unit 3 theory, demo, and practice — grouped, with a
2–3 sentence summary written so **your agent can use it as context**. Links are
external (DOI / arXiv / project pages). Paywalled items are link-only.

> How to use this with an agent: paste a summary + link into your prompt when
> you want the agent to apply a specific method ("identify the SARIMA order with
> the Box–Jenkins ACF/PACF procedure", "use a rolling-origin cross-validation
> for the walk-forward error", "compare against a strong seasonal-naive
> baseline"). The vocabulary here is the vocabulary the rubric rewards.

---

## Foundations — ARIMA / Box–Jenkins / forecasting methodology

- **Box & Jenkins (1970), "Time Series Analysis: Forecasting and Control."**
  The foundational text that defines the **ARIMA** model class and the
  identification → estimation → diagnostic-checking (Box–Jenkins) methodology the
  demo follows. It is where stationarity, differencing, and the ACF/PACF reading
  of (p, d, q) come from. Current edition: Box, Jenkins, Reinsel & Ljung, 5th ed.
  (Wiley, 2015). https://books.google.com/books/about/Time_Series_Analysis.html?id=sRzvAAAAMAAJ

- **Hyndman & Athanasopoulos (2021), "Forecasting: Principles and Practice" (3rd ed., free online).**
  The practical reference for everything in this unit: Ch. 9 (ARIMA + seasonal
  ARIMA), Sec. 9.1 (stationarity & differencing), Sec. 5.10 (time-series
  cross-validation / rolling-forecasting-origin — the demo's walk-forward), and
  Sec. 5.2 (simple benchmark methods — the historical-average and seasonal-naive
  floors). Cite a section when you want the agent to apply that exact recipe.
  https://otexts.com/fpp3/

## Traffic-specific statistical baselines

- **Williams & Hoel (2003), "Modeling and Forecasting Vehicular Traffic Flow as a Seasonal ARIMA Process."**
  Establishes the theoretical case that traffic flow is well modelled as a
  **seasonal ARIMA** with a daily/weekly period — the justification for the
  demo's `(p,d,q)(P,D,Q)_m` with a daily season. The empirical anchor for "SARIMA
  is the honest baseline on road-speed series."
  https://doi.org/10.1061/(ASCE)0733-947X(2003)129:6(664)

- **Rodrigues (2022), "On the Importance of Stationarity, Strong Baselines and Benchmarks in Transport Prediction Problems."**
  The paper behind this unit's whole stance: deep models often only *look* good
  because they are compared to weak baselines; a properly-tuned simple model
  (and correct stationarity handling) is frequently competitive. Use it to argue
  *why* breakeven-against-a-strong-floor is the right way to judge a forecast.
  https://arxiv.org/abs/2203.02954

## METR-LA / spatio-temporal bridge to Unit 5

- **Li, Yu, Shahabi & Liu (2018), "DCRNN: Diffusion Convolutional Recurrent Neural Network — Data-Driven Traffic Forecasting" (ICLR).**
  Introduces the **METR-LA** dataset the demo uses and the diffusion-convolution
  + RNN model that exploits the **spatial** signal a univariate SARIMA throws
  away. The "ten independent SARIMAs vs. one graph model" contrast (practice
  extension (a)/(d)) points straight here. https://arxiv.org/abs/1707.01926

- **Zhao et al. (2019), "T-GCN: A Temporal Graph Convolutional Network for Traffic Prediction" (IEEE T-ITS).**
  A clean GCN + GRU baseline for road-network speed forecasting — the simplest
  "graph + time" model. A good first read for what Unit 5 replaces the per-segment
  SARIMAs with. https://arxiv.org/abs/1811.05320

- **Cui et al. (2019), "Traffic Graph Convolutional Recurrent Neural Network" (IEEE T-ITS).**
  Network-scale traffic learning with a graph-convolution + recurrent stack;
  extends the T-GCN idea with a learned adjacency. Background for why the
  upstream→downstream lead you find in the practice is something a graph model can
  *learn*, not just hand-engineer. https://arxiv.org/abs/1802.07007

## Transit travel-time / bus-arrival prediction

- **Sun, Spall, Wong & Zhao (2025), "Real-time Bus Travel Time Prediction and Reliability Quantification: A Hybrid Markov Model."**
  A bus-specific travel-time predictor that also quantifies *reliability* (a
  prediction interval, not just a point) — directly relevant to the homework's
  corridor travel-time budget and to reading the SARIMA 80/95% fan as an
  operational tool. https://arxiv.org/abs/2503.05907

- **Barbeau, Pena & Labrador (2021), "An Open-Source Framework to Implement Kalman Filter Bus Arrival Predictions" (Networks and Spatial Economics).**
  Describes an adaptive **Kalman filter** over GTFS-realtime vehicle positions
  for arrival prediction (companion to the TheTransitClock project) — the
  recursive-estimation alternative to a batch-fit SARIMA. *Paywalled (Springer);
  summary from abstract + project docs.*
  https://doi.org/10.1007/s11067-021-09541-w

## Datasets, specifications & tooling

- **Open Bus / The Public Knowledge Workshop (HaSadna), 2024.**
  The SIRI real-time GPS archive of Israel's public transport (plus GTFS) — the
  source of the practice's `tlv_all.parquet` bus data.
  https://github.com/hasadna/open-bus

- **GTFS Realtime Reference (MobilityData / Google, 2024).**
  The specification for real-time transit feeds (vehicle positions, trip
  updates) — context for what a "live" version of the bus archive looks like and
  what fields a deployed forecast would consume.
  https://gtfs.org/documentation/realtime/reference/

- **StatsForecast (Nixtla, 2024).**
  The forecasting library the demo + solution use: numba-JIT `ARIMA`,
  `HistoricAverage`, `SeasonalNaive`, and a `cross_validation` walk-forward loop.
  Point your agent here for the exact API of the fixed-order SARIMA and the floor
  models. https://github.com/Nixtla/statsforecast

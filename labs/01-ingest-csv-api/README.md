# Lab 1 — Ingest a CSV (UI) and an API (Genie Code)

**Time**: 20 minutes &nbsp;•&nbsp; **Pre-requisites**: [Lab 0 — Setup](../00-setup/README.md) complete.

**Objective**: see two complementary Databricks ingestion paths in action — a point-and-click UI flow for a known file, and **Genie Code** for an API call that needs real Python. Both land the result in `petronas_aiea.ops` so the rest of the workshop can use it.

## What you will build

| Source | Path you'll create | Method |
|---|---|---|
| `commercial_summary.csv` (already in your volume) | `petronas_aiea.ops.commercial_summary` | **UI Add Data** — point-and-click |
| Open-Meteo public weather API | `petronas_aiea.ops.site_weather` | **Genie Code** in a notebook |

> 💡 *Why two paths?* The UI is fastest when the data is already a clean file. Genie Code earns its keep when the data lives behind an HTTP endpoint, an Excel sheet, or anything that needs a few lines of Python.

## 1. Ingest `commercial_summary.csv` via the UI

The setup notebook in Lab 0 staged `commercial_summary.csv` into your volume — you don't need anything on your laptop.

1. Left sidebar → **Catalog** → drill into `petronas_aiea` → `ops` → `raw_files` (volume) → `csv/`.
2. Click the file `commercial_summary.csv` to preview it.
3. Top-right of the preview → **Create table**.
4. In the Add Data form, confirm:
   - **Catalog**: `petronas_aiea`
   - **Schema**: `ops`
   - **Table name**: `commercial_summary`
   - **First row contains headers**: ✅
5. Click **Create table**.

That's it. Open the new table in **Catalog**, click the **Sample Data** tab — you should see month/site/product/revenue rows.

> 🔬 **Under the hood.** The UI generated SQL using `read_files()` and ran it on the serverless warehouse. Click **Show generated SQL** during create-table to see the exact statement — copy it into a notebook for re-runs in CI.

## 2. Open a notebook and the Genie Code panel

1. Left sidebar → **+ New** → **Notebook**.
2. Top-left of the notebook: change the default language to **Python**.
3. Top-right of the notebook: click the **Genie Code** icon (✨) to open the side panel.
4. At the bottom of the Genie pane, set the toggle to **Agent**.
5. Top-right of the pane → pencil icon → **Start a new chat**.

You should see three panels: file browser left, notebook centre, Genie Code right.

## 3. Ask Genie Code to ingest weather data from a public API

In the Genie pane, paste this prompt verbatim:

```
For each row in petronas_aiea.ops.sites, call the Open-Meteo API to get the last 7 days of daily weather for the site's latitude and longitude. The endpoint is https://archive-api.open-meteo.com/v1/archive with parameters latitude, longitude, start_date, end_date, daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,weathercode and timezone=Asia/Kuala_Lumpur.

Wait 0.2 seconds between calls to be polite. Build a single Spark dataframe with columns: site_id, observation_date, temperature_max_c, temperature_min_c, precipitation_mm, wind_speed_max_kmh, weather_code. Write it as a managed Delta table petronas_aiea.ops.site_weather. Add column comments derived from the column names.
```

Genie will plan the work and propose a few cells:

1. Read `sites` and build the API URLs.
2. Call the API in a loop and assemble a Spark dataframe.
3. Write the Delta table with comments.

Click **Allow** for each cell. The full run takes ~30–60 seconds (17 sites × 1 API call).

> 💡 We didn't tell Genie *which library* to use. It can pick `requests` or `urllib`, pandas or pure Python — that's the agentic-code lesson. Describe the **outcome**, let Genie choose the **approach**.

> 🛡️ **If Open-Meteo errors out** (rate limit or network blip), ask in the same Genie chat:
>
> ```
> The previous run hit an error. Add exponential backoff with up to 3 retries, and skip sites whose API call still fails. Log a warning row per skipped site.
> ```

## 4. Verify

In a new SQL cell, run:

```sql
SELECT 'commercial_summary' AS table_name, COUNT(*) AS rows FROM petronas_aiea.ops.commercial_summary
UNION ALL SELECT 'site_weather', COUNT(*) FROM petronas_aiea.ops.site_weather;
```

Order of magnitude: ~200 rows for `commercial_summary`, ~120 rows for `site_weather`.

In the Catalog browser, click `site_weather` → **Sample Data** — you should see one row per site per day.

## What you just learned

- **Add Data UI** turns a file in a volume into a governed Delta table with one click — no code.
- **Genie Code** is the right tool when the work needs Python — API calls, custom transforms, anything beyond `read_files()`.
- Both paths land in **Unity Catalog**, so downstream tools (Genie Spaces, agents, dashboards) treat them identically.

## Next

➡️ [Lab 2 — Apply business semantics with a Metric View](../02-business-semantics-metric-view/README.md)

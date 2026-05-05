# Lab 2 — Business semantics with a Metric View

**Time**: 15 minutes &nbsp;•&nbsp; **Pre-requisites**: [Lab 0](../00-setup/README.md) and [Lab 1](../01-ingest-csv-api/README.md) complete.

**Objective**: turn raw Delta tables into **discoverable, governed business assets** that downstream consumers — Genie Spaces, AI/BI dashboards, agents — can all read from one place. You'll do two things:

1. Apply **AI-generated table and column descriptions** (one click per table).
2. Create a **Metric View** — Unity Catalog's first-class object for declaring business measures and dimensions in YAML.

A Metric View is the actual *semantic layer* — when Genie answers "what was average uptime by BU?", it can read your metric view's definition of `avg_uptime_pct` instead of inventing one.

## 1. Apply AI-generated descriptions

Databricks can suggest table and column descriptions automatically.

1. Left sidebar → **Catalog** → drill to `petronas_aiea` → `ops` → click `operations_daily`.
2. At the top of the table page, look for **AI-generated descriptions** → click **Generate**.
3. When suggestions appear, click **Apply** for the table description and **Apply all** for the columns.
4. Repeat for `assets`, `commercial_summary`, `sites`, `site_weather`.

> ⚠️ **Always review the AI's suggestions.** They're a strong starting point but won't know your internal business logic — for that, the Metric View below is the better tool.

## 2. Create a Metric View via Genie Code

Open a notebook (any language — set top-left to **Python** or **SQL**, doesn't matter) and open the **Genie Code** pane.

In the Genie pane, paste this prompt:

```
Create a Metric View called petronas_aiea.ops.operations_metrics on top of petronas_aiea.ops.operations_daily, joined to petronas_aiea.ops.sites on site_id so we can dimension by business_unit, site_type and country from the dimension table.

Dimensions:
- business_unit (from sites)
- site_type (from sites)
- country (from sites)
- operation_date (from operations_daily)

Measures:
- total_throughput = SUM(throughput_value)
- avg_uptime_pct = AVG(uptime_pct)
- total_emissions_tco2e = SUM(emissions_tco2e)
- total_energy_mwh = SUM(energy_consumed_mwh)
- energy_intensity = SUM(energy_consumed_mwh) / NULLIF(SUM(throughput_value), 0)

Use the CREATE VIEW ... WITH METRICS LANGUAGE YAML syntax. Add a comment "Governed business metrics for PETRONAS daily operations".
```

Click **Allow**. Genie writes a `CREATE OR REPLACE VIEW … WITH METRICS LANGUAGE YAML AS $$ … $$` statement and runs it.

> 📚 **Reference**: [Create and edit metric views](https://docs.databricks.com/aws/en/business-semantics/metric-views/create-edit). Metric Views are queryable like normal views and are auto-discovered by Genie Spaces, AI/BI Dashboards and SQL editors.

## 3. Query the Metric View

In a new SQL cell, run:

```sql
SELECT business_unit,
       MEASURE(avg_uptime_pct) AS avg_uptime_pct,
       MEASURE(total_emissions_tco2e) AS total_emissions_tco2e,
       MEASURE(energy_intensity) AS energy_intensity
FROM   petronas_aiea.ops.operations_metrics
GROUP BY business_unit
ORDER BY avg_uptime_pct DESC;
```

You should see one row per BU. Try a different grain:

```sql
SELECT site_type,
       MEASURE(avg_uptime_pct) AS avg_uptime_pct,
       MEASURE(energy_intensity) AS energy_intensity
FROM   petronas_aiea.ops.operations_metrics
GROUP BY site_type;
```

Same definitions, different cut. **That's the point** — you wrote `avg_uptime_pct` once, every consumer gets the same answer.

## 4. (60 seconds) Tour the lineage tab

1. **Catalog** → `petronas_aiea` → `ops` → `operations_metrics`.
2. Click the **Lineage** tab.
3. You should see the upstream tables (`operations_daily`, `sites`) feeding the metric view, and the notebook that built it.

> 🧭 **Lineage is automatic.** You didn't add anything to capture it — every Spark/SQL execution updates UC lineage in the background. Same lineage the Group Data Office would inspect for an audit.

## What you just learned

- **AI-generated descriptions** are a one-click way to bootstrap UC metadata. Treat them as a starting point.
- A **Metric View** is the proper *semantic layer* — dimensions + measures defined once, in YAML, governed by Unity Catalog.
- The metric view shows up automatically in Genie's catalog awareness — you'll see this in Lab 3.
- **Lineage** comes for free with every execution.

## Next

➡️ [Lab 3 — Build the PETRONAS Ops Genie Space](../03-genie-space/README.md)

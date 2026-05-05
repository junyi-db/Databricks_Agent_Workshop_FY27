# Lab 3 — Build the PETRONAS Ops Genie Space

**Time**: 20 minutes &nbsp;•&nbsp; **Pre-requisites**: Labs 0, 1, 2 complete.

**Objective**: stand up a Genie Space called **"PETRONAS Ops Genie"** over the operational tables and metric view, curate it with a few business rules, and see Chat vs Agent mode in action.

## What is a Genie Space

A Genie Space is a **conversational interface** over Unity Catalog tables, views and metric views. Users ask plain-language questions; Genie translates to SQL, runs it on a SQL warehouse, and answers in tables and charts. It's the right entry point for your business stakeholders — not a tool for engineers.

## 1. Create the Space

1. Left sidebar → **Genie**.
2. **+ New**.
3. **Connect your data** — type and select each of:
   - `petronas_aiea.ops.operations_daily`
   - `petronas_aiea.ops.sites`
   - `petronas_aiea.ops.assets`
   - `petronas_aiea.ops.commercial_summary`
   - `petronas_aiea.ops.site_weather`
   - `petronas_aiea.ops.operations_metrics` *(the Metric View from Lab 2)*
4. Click **Create**.
5. **Rename** the space to `PETRONAS Ops Genie`.
6. **Description** (top of page → edit pencil): *"Ask questions about PETRONAS operational performance across business units. Answers throughput, uptime, energy intensity, emissions, asset integrity and commercial volume questions."*

## 2. Try it in Chat mode

Make sure the chat-box toggle reads **Chat** (fast, one-shot SQL). Ask:

```
How many sites do we have, and what business units are represented?
```

Click **Show code** to see the SQL Genie ran.

Try a few more — these should all work without curation:

```
What was the average uptime by business unit in the last 30 days of data?
```

```
Which 5 sites had the most outage days in the last 30 days?
```

```
For Trading and Retail, what is the total revenue by product in the latest available month?
```

> 💡 Notice that for the uptime question, Genie uses your **`operations_metrics`** Metric View — that's the Lab 2 investment paying off. Click **Show code** to confirm.

## 3. Switch to Agent mode for harder questions

Toggle the chat from **Chat** to **Agent**. Ask something open-ended:

```
Investigate why Bintulu LNG throughput varied last week. Look at uptime, weather conditions, and any inspection events overlapping that period. Tell me the most likely explanation and where it shows up most strongly in the data.
```

Watch the **Thinking…** trace stream. Agent mode plans the analysis, runs multiple queries in parallel, and synthesises a report with citations back to the SQL it ran. Expand the citations to verify any answer.

> 💡 **When to use which:**
>
> - **Chat** — known question shape, one quick chart. *"What was X?"*
> - **Agent** — open-ended exploration. *"Why is X happening?"* / *"Find patterns in Y."*

## 4. Curate with general instructions

Even with great UC metadata and a metric view, Genie benefits from a few business-specific rules. In the space settings (top-right gear icon) → **Instructions** → **General Instructions**, paste:

```
Business definitions:
- An "underperforming" or "missed target" site has throughput_value < 0.9 * throughput_target on a given day.
- A "high emitter" site is in the top decile of emissions_tco2e for its site_type.
- An "overdue inspection" is an asset whose next_inspection_date is before today and status is 'In Service'.
- "Last quarter" means the most recent calendar quarter relative to MAX(operation_date) in operations_daily.

Reporting rules:
- Throughput is NOT directly comparable across site_type because units differ. When comparing across BUs use uptime_pct or normalised energy_intensity from petronas_aiea.ops.operations_metrics instead.
- When asked about throughput always include throughput_unit in the answer.
- Use the sites dimension table when listing sites; do NOT SELECT DISTINCT site_id FROM operations_daily.
- For revenue, use commercial_summary.revenue_musd. Do NOT estimate revenue from operations_daily.
```

Click **Save**, then start a **New chat** and ask:

```
What proportion of all site-days are underperforming, and which BU has the highest rate?
```

Genie should apply your business definition without being told again.

## 5. Verification

You're done when:

- [ ] `PETRONAS Ops Genie` space exists and is connected to your tables + metric view.
- [ ] You can ask "average uptime by BU" and get a numeric answer.
- [ ] General Instructions are saved.
- [ ] At least one Agent-mode question runs without errors.

## Next

➡️ [Lab 4 — Knowledge Assistant on the PDFs](../04-agent-bricks-ka/README.md)

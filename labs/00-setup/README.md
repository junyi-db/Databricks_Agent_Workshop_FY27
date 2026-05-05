# Lab 0 — Setup

**Time**: 15 minutes &nbsp;•&nbsp; **Pre-requisites**: a laptop with a modern browser, plus access to your **Databricks Trial** workspace.

**Objective**: get into your Databricks workspace, create a brand-new Unity Catalog catalog called `petronas_aiea`, then run a one-click setup notebook that seeds the workshop tables and stages the workshop files. By the end of this lab the catalog browser shows `petronas_aiea.ops` with three tables and a populated volume.

> 💡 Throughout these labs we use **Genie Code** — Databricks' built-in AI partner — to write SQL and Python for us. You don't memorise syntax; you describe what you want, Genie writes, you click *Allow*.

## 1. Sign in to your Databricks Trial workspace

Use the workspace URL provided by your workshop host. Sign in with the email that was added to the workspace invite.

When the home screen loads, take 30 seconds to look around the **left sidebar** — you'll be using **Catalog**, **Genie**, **Agents** and **Compute → Apps** today.

> 🔧 **Compute check.** In the top-right of the sidebar, click **Compute → SQL warehouses** and confirm that the **Serverless Starter Warehouse** is **Running** (or click **Start**). Genie Code uses this warehouse under the hood.

## 2. Create the `petronas_aiea` catalog

A **catalog** is the top-level container in Unity Catalog — above schemas, tables and volumes. Creating one is a privilege Trial gives you out of the box.

1. Left sidebar → **Catalog**.
2. Top-right of the catalog browser → **+** → **Create a catalog**.
3. Fill in:
   - **Catalog name**: `petronas_aiea`
   - **Type**: **Standard**
   - **Storage location**: leave blank (uses workspace default).
   - **Comment**: *PETRONAS AIEA Workshop — cross-BU operational data*
4. Click **Create**.

You should now see `petronas_aiea` listed alongside the built-in catalogs (`main`, `samples`, `system`).

> 🧭 **Why a new catalog?** In production you'd put each domain or BU in its own catalog so permissions, tags and lineage stay scoped. This is the same pattern PETRONAS would use for `petronas_upstream`, `petronas_trading`, etc.

## 3. Import and run the workshop setup notebook

Instead of clicking through 8 separate "create schema / create volume / upload file" steps, we'll run one notebook that does it all.

1. Left sidebar → **Workspace** → click the dropdown chevron next to your home folder → **Import**.
2. Pick **URL** and paste:

```
https://raw.githubusercontent.com/junyi-db/Databricks_Agent_Workshop_FY27/main/labs/00-setup/workshop_setup.py
```

3. Click **Import**. The notebook opens.
4. Top-right → click **Run all** (▷▷).
5. Wait ~60 seconds. You'll see green checkmarks per cell as it:
   - Creates schema `ops` and volume `raw_files` inside `petronas_aiea`
   - Loads `operations_daily`, `sites` and `assets` Delta tables
   - Stages `commercial_summary.csv` and 5 PDFs into the volume

The last cell prints a `SHOW TABLES` result — three tables.

> ⚙️ **What just happened.** The notebook used `pandas.read_csv` over public GitHub URLs to land the data, then wrote managed Delta tables. Same pattern works for ingesting from any HTTPS endpoint — you'll see Genie Code do this with an API in Lab 1.

## 4. Verification

You're done with setup when all four are true:

- [ ] **Catalog** browser shows `petronas_aiea`.
- [ ] Inside it, schema `ops` contains `operations_daily`, `sites`, `assets`.
- [ ] Volume `petronas_aiea.ops.raw_files` contains a `csv/` and a `pdfs/` folder.
- [ ] Running `SELECT COUNT(*) FROM petronas_aiea.ops.operations_daily` in any SQL cell returns ~3,000.

If anything is off, ask Genie Code in any notebook:

```
What's the SQL to check whether catalog/schema/table X exists in Unity Catalog?
```

## Next

➡️ [Lab 1 — Ingest a CSV (UI) and an API (Genie Code)](../01-ingest-csv-api/README.md)

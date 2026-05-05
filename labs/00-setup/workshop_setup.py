# Databricks notebook source
# MAGIC %md
# MAGIC # PETRONAS AIEA Workshop — One-Click Setup
# MAGIC
# MAGIC This notebook sets up everything you need for the workshop:
# MAGIC
# MAGIC 1. Creates a new **catalog** `petronas_aiea`, schema `ops`, volume `raw_files`.
# MAGIC 2. Seeds three Delta tables (`operations_daily`, `sites`, `assets`) from the workshop GitHub repo.
# MAGIC 3. Stages a CSV (`commercial_summary.csv`) and 5 PDFs into the volume so later labs have files to ingest.
# MAGIC
# MAGIC **How to run:** click **Run all** (▷▷ at the top of the notebook).
# MAGIC Total runtime: ~60 seconds on a serverless warehouse.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration
# MAGIC Change `CATALOG_NAME` only if your metastore admin asks you to.

# COMMAND ----------

CATALOG_NAME = "petronas_aiea"
SCHEMA_NAME  = "ops"
VOLUME_NAME  = "raw_files"

GITHUB_RAW = "https://raw.githubusercontent.com/junyi-db/Databricks_Agent_Workshop_FY27/main"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Create catalog, schema, volume
# MAGIC In Databricks Trial your first user is the metastore admin, so this works out of the box.

# COMMAND ----------

spark.sql(f"CREATE CATALOG IF NOT EXISTS {CATALOG_NAME} COMMENT 'PETRONAS AIEA Workshop — cross-BU operational data'")
spark.sql(f"CREATE SCHEMA  IF NOT EXISTS {CATALOG_NAME}.{SCHEMA_NAME} COMMENT 'Operational tables for the AIEA workshop'")
spark.sql(f"CREATE VOLUME  IF NOT EXISTS {CATALOG_NAME}.{SCHEMA_NAME}.{VOLUME_NAME} COMMENT 'Raw workshop files — CSVs and PDFs'")

print(f"✅ Created  {CATALOG_NAME} / {SCHEMA_NAME} / {VOLUME_NAME}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Seed Delta tables from the workshop GitHub repo
# MAGIC We deliberately leave `commercial_summary` for you to ingest yourself in Lab 1.

# COMMAND ----------

import pandas as pd

def load_csv_to_delta(filename: str, table_name: str) -> None:
    pdf = pd.read_csv(f"{GITHUB_RAW}/data/csv/{filename}")
    sdf = spark.createDataFrame(pdf)
    sdf.write.mode("overwrite").saveAsTable(f"{CATALOG_NAME}.{SCHEMA_NAME}.{table_name}")
    print(f"   {table_name}: {sdf.count():,} rows")

print("Loading tables...")
load_csv_to_delta("operations_daily.csv", "operations_daily")
load_csv_to_delta("assets_flat.csv",      "assets")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Build the `sites` dimension
# MAGIC One row per site, derived from `operations_daily`. Lab 3's Genie Space relies on this.

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE TABLE {CATALOG_NAME}.{SCHEMA_NAME}.sites
COMMENT 'PETRONAS operational sites — one row per site_id'
AS
SELECT
    site_id,
    MAX(site_name)         AS site_name,
    MAX(business_unit)     AS business_unit,
    MAX(site_type)         AS site_type,
    MAX(country)           AS country,
    MAX(latitude)          AS latitude,
    MAX(longitude)         AS longitude,
    MAX(throughput_unit)   AS throughput_unit,
    AVG(throughput_target) AS throughput_target
FROM {CATALOG_NAME}.{SCHEMA_NAME}.operations_daily
GROUP BY site_id
""")

count = spark.table(f"{CATALOG_NAME}.{SCHEMA_NAME}.sites").count()
print(f"   sites: {count} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Stage `commercial_summary.csv` and the PDFs into the volume
# MAGIC - **CSV** is for Lab 1's UI-driven ingestion exercise.
# MAGIC - **PDFs** are for Lab 4's Knowledge Assistant.

# COMMAND ----------

import os, urllib.request

VOLUME_PATH = f"/Volumes/{CATALOG_NAME}/{SCHEMA_NAME}/{VOLUME_NAME}"

def fetch(rel_url: str, dest_path: str) -> None:
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    urllib.request.urlretrieve(f"{GITHUB_RAW}/{rel_url}", dest_path)
    print(f"   {dest_path}")

print("Staging CSV for Lab 1...")
fetch("data/csv/commercial_summary.csv", f"{VOLUME_PATH}/csv/commercial_summary.csv")

print("\nStaging PDFs for Lab 4...")
PDFS = [
    "01_operational_excellence_sop.pdf",
    "02_net_zero_2050_brief.pdf",
    "03_asset_integrity_policy.pdf",
    "04_production_reporting_standard.pdf",
    "05_compressor_maintenance_manual.pdf",
]
for pdf in PDFS:
    fetch(f"data/pdfs/{pdf}", f"{VOLUME_PATH}/pdfs/{pdf}")

print(f"\n✅ Volume populated at {VOLUME_PATH}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Setup complete
# MAGIC
# MAGIC You now have:
# MAGIC - Catalog **`petronas_aiea`** with schema **`ops`**
# MAGIC - Tables: `operations_daily`, `sites`, `assets`
# MAGIC - Volume **`raw_files`** containing `csv/commercial_summary.csv` and 5 PDFs in `pdfs/`
# MAGIC
# MAGIC Head back to **Lab 0 — Setup** in the workshop README to verify and continue.

# COMMAND ----------

display(spark.sql(f"SHOW TABLES IN {CATALOG_NAME}.{SCHEMA_NAME}"))

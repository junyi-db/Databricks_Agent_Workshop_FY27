# PETRONAS AI Enterprise Adoption Workshop

End-to-end Databricks hands-on workshop for the PETRONAS AIEA cohort. Participants build a cross-business-unit operational data product on the Databricks Data Intelligence Platform — from raw ingestion to a production-ready AI agent — in a Databricks Trial workspace.

## What you will build

A **PETRONAS Operations Co-Pilot** that lets any business user ask plain-language questions about operational performance — and gets answers backed by either live data or company policy.

Under the hood, by the end of the afternoon you will have stood up:

- A **Unity Catalog** catalog (`petronas_aiea`) with bronze tables and a Metric View — seeded by a one-click setup notebook plus one UI ingestion and one API ingestion you do yourself.
- A **Genie Space** (`PETRONAS Ops Genie`) over the operational tables, with curated business definitions.
- An **Agent Bricks Knowledge Assistant** (`PETRONAS_Operations_KA`) over operational SOPs, the Net Zero brief and equipment manuals stored in a UC Volume.
- An **Agent Bricks Multi-Agent Supervisor** (`PETRONAS_Operations_CoPilot`) that routes questions to the right agent.
- *(Optional)* A **Databricks App** built from the **"Chat UI for Existing Agent"** template — a branded chat UI in front of the supervisor, deployable to anyone in the workspace.

All of it is governed by Unity Catalog with column-level lineage and AI-generated descriptions — so the same agent answers come from the same governed tables when you take this back to your real business unit.

## Audience

- PETRONAS AI Enterprise Adoption (AIEA) workshop participants — Solutions Architects, Data Engineers, Analysts, and Business Stakeholders from Upstream, Downstream, Gas, Trading, Retail and Logistics.
- ~20 participants, mixed technical depth.
- No prior Databricks experience required for the morning. The afternoon hands-on labs assume basic SQL and willingness to copy-paste prompts.

## Workshop format

- **Morning** — keynotes + Databricks 101 + UC / Lakeflow Designer demo (presentation-led).
- **Afternoon (14:00–16:00)** — self-paced hands-on labs in a **Databricks Trial** workspace.
- **End of day** — next steps, AI POC Forum / Office Hours, Use Case Coaching.

See [`AGENDA.md`](./AGENDA.md) for the full schedule.

## Sample data theme

We use a single cross-functional theme — **PETRONAS Operations Intelligence** — so every learner finds their own business unit in the data.

| File | Contents | BUs |
|---|---|---|
| `data/csv/operations_daily.csv` | Daily ops metrics (throughput, uptime, energy, emissions) | All |
| `data/csv/commercial_summary.csv` | Monthly cargo / sales / trade volumes | Trading, Retail, Downstream, Logistics |
| `data/csv/assets_flat.csv` | Asset register, flattened across BUs | All |
| `data/pdfs/*.pdf` | 5 synthetic operational policies & manuals | All |
| Open-Meteo public API | Weather at site coordinates | Upstream, Logistics |

All data is **synthetic** and prepared solely for this workshop. It does not represent real PETRONAS operational data. The Lab 0 setup notebook pulls these files from this GitHub repo automatically — there are no laptop downloads.

## Repository layout

```
Databricks_Agent_Workshop_FY27/
├── README.md                                  ← you are here
├── AGENDA.md                                  ← full-day schedule
├── labs/
│   ├── 00-setup/                              ← Trial signin, new catalog, one-click setup notebook
│   │   └── workshop_setup.py                  ← Databricks notebook that seeds tables + stages files
│   ├── 01-ingest-csv-api/                     ← UI Add Data + Genie Code over Open-Meteo
│   ├── 02-business-semantics-metric-view/     ← AI descriptions + Metric View
│   ├── 03-genie-space/                        ← Build "PETRONAS Ops Genie"
│   ├── 04-agent-bricks-ka/                    ← Build "PETRONAS_Operations_KA"
│   ├── 05-multi-agent-supervisor/             ← Combine into Co-Pilot (finale)
│   └── 06-deploy-databricks-app/              ← (optional) "Chat UI for Existing Agent" template
├── data/                                      ← prepared sample files (auto-fetched by the setup notebook)
├── slides/                                    ← Speaker slide content (markdown)
└── scripts/                                   ← Helpers used to generate the sample data
```

## Prerequisites

1. A laptop with a modern browser (Chrome / Edge / Safari).
2. Access to your **Databricks Trial** workspace (the workshop host will share the URL and an invite to your email).
3. That's it — no local install, no `git clone`, no CLI.

## How to use this repo on the day

The morning is presentation-led; you don't need this repo open. After lunch, follow each lab in `labs/` in numerical order. Every lab starts with **Objective**, **Pre-requisites** and **What you'll build**, and ends with a clear **Verification** so you know you finished cleanly.

If you fall behind during the workshop, every lab is fully self-contained — you can keep going at home on your own pace. The Trial workspace stays available for the duration of the trial.

## Acknowledgements

Lab structure inspired by the public **Genie Code Workshop Labs** — adapted for the PETRONAS AIEA cohort with cross-BU operational data and an agent-app build-out.

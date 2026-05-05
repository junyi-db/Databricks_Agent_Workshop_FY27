# Lab 5 — Multi-Agent Supervisor: PETRONAS Operations Co-Pilot

**Time**: 15 minutes &nbsp;•&nbsp; **Pre-requisites**: Genie Space from [Lab 3](../03-genie-space/README.md) and KA from [Lab 4](../04-agent-bricks-ka/README.md).

**Objective**: combine the **Genie Space** (live operational data) and the **Knowledge Assistant** (policies and manuals) into a single supervisor agent — `PETRONAS Operations Co-Pilot` — that routes each question to the right tool and returns one coherent answer. This is the **finale** of the workshop.

## Why a supervisor

Each agent is great at one thing:

- **Genie** can answer *"How many Tier-1 incidents last quarter?"* — but can't tell you the procedure for a Tier-1 incident.
- **KA** can answer *"What's the Net Zero target?"* — but can't compute the current emissions intensity for the Pengerang refinery.

A **Multi-Agent Supervisor (MAS)** sits in front of both. The user asks one question; the supervisor decides which agent — or both — to call, then composes a single answer with citations from each tool.

## 1. Build a supervisor

1. Left sidebar → **Agents** → **+ Build a new agent** → **Multi-Agent Supervisor**.

## 2. Configure the supervisor

Fill in:

- **Name**: `PETRONAS_Operations_CoPilot`
- **Description**: *"PETRONAS Operations Co-Pilot. Answers questions about live operational performance and operational policy by routing to the Ops Genie and the Operations Knowledge Assistant."*

### Add agent 1 — Genie Space

- Click **+ Add agent**.
- **Type**: **Genie Space**.
- **Genie Space**: select `PETRONAS Ops Genie`.
- **Agent name**: `ops_genie`
- **When to use**: *"Use for quantitative questions about operational performance: throughput, uptime, energy consumption, emissions, asset criticality counts, commercial volume, revenue, or any question that boils down to running SQL on live tables."*

### Add agent 2 — Knowledge Assistant

- **+ Add agent**.
- **Type**: **Knowledge Assistant**.
- **Knowledge Assistant**: select `PETRONAS_Operations_KA` (from Lab 4).
- **Agent name**: `ops_ka`
- **When to use**: *"Use for questions about operational policies, definitions, procedures, targets, sustainability commitments, asset integrity rules, or how to do something. Returns answers grounded in PETRONAS SOPs, the Net Zero 2050 brief, and the equipment maintenance manual."*

### Supervisor instructions

```
You are the PETRONAS Operations Co-Pilot.

Routing rules:
1. If the question is about specific live numbers (throughput, uptime, emissions today, asset counts, revenue), call ops_genie.
2. If the question is about a procedure, definition, target, policy, or how-to, call ops_ka.
3. If the question requires both (e.g., "Show last week's underperforming sites and tell me the variance investigation procedure"), call ops_genie first to get the data, then call ops_ka for the procedure, and combine into one answer.

Style:
- Always include data citations from ops_genie when present (Show the SQL on request).
- Always cite document names from ops_ka when present.
- British English, concise, professional.
```

Click **Create**. The supervisor goes through PROVISIONING (1–3 minutes).

## 3. Test the routing — the finale

When the supervisor reads **ONLINE**, in the **Test** tab paste each of the below and watch which agent fires:

| Question | Should call | Why |
|---|---|---|
| `Average uptime by business unit last month?` | `ops_genie` | Numeric, live data |
| `What is our Net Zero scope 1 target by 2030?` | `ops_ka` | Policy question |
| `Which 3 sites had the lowest uptime last week, and what is the variance investigation procedure I should follow?` | **both** | Live data **+** procedure |
| `Are any Critical assets overdue for inspection, and what's the escalation path?` | **both** | Asset query **+** policy |

🎉 The multi-agent questions are the demo moment. The supervisor returns one structured answer with **a SQL citation and a document citation in the same message**. Take a screenshot — that's the workshop deliverable.

## 4. Note the serving endpoint name

From the supervisor's page, find the **serving endpoint** — its name looks like `agents_petronas_aiea_ops_petronas_operations_copilot` (or similar). You'll point the optional Lab 6 app at it.

## What you just learned

- An **Agent Bricks Multi-Agent Supervisor** orchestrates multiple specialised agents — Genie Spaces, Knowledge Assistants, custom model serving endpoints, UC functions — through one endpoint.
- Routing is driven by each agent's **description** plus the supervisor's **instructions**. Get those right and the rest works.
- The supervisor exposes a standard chat-completion-style endpoint, so any UI can call it.

## Next

➡️ [Lab 6 (optional) — Deploy as a Databricks App](../06-deploy-databricks-app/README.md)

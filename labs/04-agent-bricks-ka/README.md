# Lab 4 — Build the PETRONAS Operations Knowledge Assistant

**Time**: 20 minutes (≈10 active + ≈5 indexing in background + buffer) &nbsp;•&nbsp; **Pre-requisites**: [Lab 0](../00-setup/README.md) complete (PDFs are already in your volume).

**Objective**: stand up an **Agent Bricks Knowledge Assistant (KA)** that answers questions about PETRONAS operational policies, the Net Zero brief, the asset integrity policy and the equipment manual — grounded in the PDFs your Lab 0 setup notebook staged into the volume.

> 🤖 **What is a Knowledge Assistant?** Agent Bricks pre-builds a managed RAG agent: it parses your PDFs, chunks them, embeds the chunks, builds a vector index, deploys a serving endpoint, and exposes a chat UI — all from one form. You don't write any retrieval code. We use this in Lab 5 as one tool in our supervisor.

## 1. Open Agent Bricks

1. Left sidebar → **Agents**.
2. **+ Build a new agent** → **Knowledge Assistant**.

## 2. Configure the KA

Fill in the form:

- **Name**: `PETRONAS_Operations_KA`
- **Description**: *"Knowledge Assistant for PETRONAS operational policies, sustainability targets, asset integrity policies and equipment manuals. Answers questions about procedures, definitions, targets, and how to do something."*
- **Knowledge sources** → **Add knowledge source** → **Volume**:
  - Volume path: `/Volumes/petronas_aiea/ops/raw_files/pdfs`
  - Click **Add**.
- **Instructions** (how the KA should answer):

```
You are a PETRONAS Group Operational Excellence advisor. Answer using only the provided documents.

Always cite the specific document name in your answer (e.g., "per the Operational Excellence SOP" or "per the Net Zero 2050 Brief").

If the question is about quantitative live data (specific throughput numbers, individual site uptime, today's emissions), say that's better answered by the PETRONAS Ops Genie and suggest a question to ask there.

Use British English. Be concise: 3-5 sentences for short questions, bullet points for procedures.
```

Click **Create**.

## 3. While indexing — read ahead

The KA goes into **PROVISIONING** for 2–5 minutes while Databricks parses, chunks, embeds and indexes the PDFs and deploys an endpoint of the form `ka-<id>-endpoint`.

> ☕ Use this time to skim [Lab 5 — Multi-Agent Supervisor](../05-multi-agent-supervisor/README.md). When the KA reads **ONLINE**, come back here.

## 4. Test the KA

In the **Test** tab, paste each of the following:

```
What is our Group Scope 1 reduction target by 2030?
```

Expected: cites the *Net Zero 2050 Brief*; returns the 25% reduction vs 2019 baseline.

```
A Critical asset is overdue for inspection — what should I do?
```

Expected: cites the *Asset Integrity Management Policy*; lists the escalation within 24 hours and the deviation approval requirement.

```
What is the daily walkdown checklist for a centrifugal gas compressor?
```

Expected: cites the *Compressor Maintenance Manual*; lists the four daily checks.

```
What was Bokor Platform A's throughput last week?
```

Expected: KA correctly defers — *"this is a question for the PETRONAS Ops Genie."*

## 5. Note the KA name

You'll select this KA by name in Lab 5 — it appears in the supervisor's "Add agent" dropdown as `PETRONAS_Operations_KA`. You don't need to copy any IDs.

## What you just learned

- Knowledge Assistants are **the easy button for RAG over a volume of documents**. No chunking, embedding, indexing or serving code.
- The KA's **instructions** are where you encode tone, citation rules, and what *not* to answer.
- The KA hands off cleanly to other agents — in Lab 5 the supervisor will route quantitative questions to Genie and policy questions to the KA.

> 🚀 **Take-home upgrade.** Swap the synthetic PDFs in your volume for your BU's real SOPs and rebuild the KA — same pattern, your data.

## Next

➡️ [Lab 5 — Combine into the Multi-Agent Supervisor](../05-multi-agent-supervisor/README.md)

# Lab 6 (optional) — Deploy the Co-Pilot as a Databricks App

**Time**: 10 minutes &nbsp;•&nbsp; **Pre-requisites**: [Lab 5](../05-multi-agent-supervisor/README.md) supervisor is **ONLINE** with a serving endpoint.

> 🟡 **Optional.** If you're running short on time, watch your workshop host's pre-deployed app demo and skip this lab — every step uses a built-in template, so you can do this at home in under 10 minutes.

**Objective**: deploy a hosted, branded chat UI that any workspace user can open in their browser — backed by the Multi-Agent Supervisor you built in Lab 5. Zero code: we'll use the Databricks-Apps **"Chat UI for Existing Agent"** template.

> 🚀 **What is a Databricks App?** A Databricks App is a Python web app deployed inside your workspace. It runs as a service principal, authenticates users via SSO, and can call any model serving endpoint or UC asset that the service principal has access to.

## 1. Create the app from a template

1. Left sidebar → **Compute** → **Apps** tab → **+ Create app**.
2. Scroll to **Install from a template** → click the **Agents** tab.
3. Pick the **Chat UI for Existing Agent** card. *("Deploy a production chat interface for an agent or model endpoint you've already built.")*
4. Click **Use template**.

## 2. Configure the app

The template form asks for very little:

- **App name**: `petronas-operations-copilot`
- **Description**: *PETRONAS Operations Co-Pilot — chat UI for the multi-agent supervisor*
- **Serving endpoint** (the only required dependency): pick the supervisor endpoint from Lab 5 (its name looks like `agents_petronas_aiea_ops_petronas_operations_copilot` or similar).

Click **Create and deploy**. The app provisions in 2–3 minutes.

> 🔐 **What just happened with permissions.** The template auto-creates a service principal for the app and grants it **Can Query** on the supervisor endpoint. No manual permission grants needed — that's the lift the template gives you over a custom build.

## 3. Use the app

1. When the status reads **Running**, click **Open app** on the app page.
2. SSO logs you in as the same identity you used for Databricks.
3. Try the dual-citation questions from Lab 5:

```
Are any Critical assets overdue for inspection, and what's the escalation path I should follow?
```

```
Show me last week's underperforming sites and tell me the variance investigation procedure.
```

```
What is our Group Scope 1 target by 2030 and which BU has the highest emissions intensity right now?
```

You should see one consolidated answer per question — citations from Genie SQL **and** the KA documents both visible.

## 4. (Optional) Share the URL

The app URL is workspace-scoped. Anyone with workspace access and the **Can Use** permission on the app can open it. Share via:

1. App page → **Permissions** tab → **Grant access** → pick a user or group → **Can Use**.
2. Copy the app URL from the top of the app page and share.

## What you just learned

- The **Chat UI for Existing Agent** template turns an agent endpoint into a branded, SSO-protected chat app in minutes — no custom backend or frontend.
- The app runs as a **service principal**, so it has its own UC permissions and is auditable like any other identity.
- Production pattern: Genie + KA + Supervisor + App, all governed by Unity Catalog.

## Wrap up

You now have a fully working operations co-pilot you could share with a colleague today. 🎉

What you'd typically do next in a real engagement:

- **Add more agents** — a Salesforce ticket-creation agent, a forecasting agent, a cost-analysis agent.
- **Wire in real source-of-truth tables** via Lakeflow Connect on a schedule.
- **Add evaluation** with `mlflow.evaluate` and `databricks.agents.evaluate` to track answer quality over time.
- **Roll out to a wider audience** — share the app URL, monitor usage in **System Tables**.

Take the URL home.

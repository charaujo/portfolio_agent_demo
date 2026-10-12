# AI Project Portfolio Analyst — Office Hour Demo

A Microsoft Foundry **model deployment** drives an agent implemented in Python with tool calling. This is NOT a managed Foundry Agent Service agent, and the policy lookup is NOT vector-based RAG.

## Prerequisites

- Python 3.11 or newer and `pip`.
- A Microsoft Foundry project/resource, a deployed model that supports **chat completions with function/tool calling**, its deployment name, an Azure OpenAI v1-compatible endpoint, and an API key. Model usage may incur Azure charges.
- Internet access to the configured Foundry endpoint for agent chat. The portfolio and policy views use the included synthetic data; no database is required.

## Foundry setup (10–20 minutes, assuming you already have a subscription)

1. Open https://ai.azure.com/ and select/create a Foundry project and resource.
2. Go to **Models + endpoints / Model catalog** (label may vary) and deploy a model that supports **chat completions and function/tool calling**. `gpt-4.1-mini` is a good choice if available in your region/subscription.
3. Choose a standard pay-as-you-go deployment where available. Copy the **deployment name** (not merely the model family name).
4. From the resource's **Keys and Endpoint** area, retrieve its API key and Azure OpenAI v1-compatible endpoint. A typical endpoint is `https://YOUR-RESOURCE.openai.azure.com/openai/v1/`. Some Foundry resources use `https://YOUR-RESOURCE.services.ai.azure.com/openai/v1/`. Use the actual endpoint provided for your deployment.
5. Duplicate `.env.example` as `.env` and set the three variables. **Do not upload or screen-share your .env file.**
6. Confirm you can query your deployment in the Foundry playground before starting Streamlit.

## Local setup (Windows PowerShell)

Run these commands from the directory containing `app.py` and `requirements.txt` (after cloning the repository, change into `portfolio_agent_demo`):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
python test_local.py
python -m streamlit run app.py
```

For macOS/Linux, from the same directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Foundry deployment details before using the agent.
python test_local.py
python -m streamlit run app.py
```

In `.env`, set `FOUNDRY_ENDPOINT` to the actual endpoint ending in `/openai/v1/`, `FOUNDRY_API_KEY` to the resource API key, and `FOUNDRY_DEPLOYMENT` to your **deployment name** (not necessarily the model name). The example values are placeholders and will not connect. Open the local URL printed by Streamlit (usually `http://localhost:8501`). `test_local.py` checks the included data and policy without calling Foundry; the chat requires valid Foundry credentials. The optional `test_foundry.py` checks a live Foundry connection using the Responses API and requires a deployment that supports that API.

## Live demo script

1. Ask: `Which projects require escalation? Apply the policy and cite project IDs and rules.`
2. Open the **Agent trace & audit** tab and show actual calls to `evaluate_portfolio` and `get_policy`.
3. Ask: `Does P-108 require management escalation? Explain why or why not.` (Missing owner requires remediation, not escalation.)
4. Ask: `Prepare an escalation for P-101 to request a recovery plan.`
5. Show the **Human approval required** box. Reject it first; explain nothing happened.
6. Repeat step 4 and approve; show the local audit log.
7. Open **Portfolio** and **Governance policy** tabs to show structured vs unstructured evidence.

## What is real vs simulated?

- **Real:** Live model inference through Microsoft Foundry, model-initiated tool calls, deterministic policy calculations, proposal creation, Streamlit approval gate, and a local JSONL audit log.
- **Simulated:** Company/project data, policy, project date (fixed at 2026-10-09), and the downstream task destination (local JSONL file, not Planner/Smartsheet).
- **Not implemented:** Managed Foundry Agent Service, Azure AI Search/vector RAG, enterprise identity/RBAC, persistent multi-user sessions, distributed tracing, or external action connectors.

## Troubleshooting

- **401/403:** Check key, endpoint, resource permissions, and whether key-based auth is allowed.
- **404 deployment not found:** `FOUNDRY_DEPLOYMENT` must exactly match the deployed model name.
- **400 tool calling unsupported:** Choose a chat-completions deployment that supports function calling.
- **Connection errors:** Confirm `/openai/v1/` endpoint and resource network restrictions.
- **Model tool-call loop:** Ask a narrower question; app limits the number of rounds.

## Security

This is a local training demo, not production software. Use fictional records, never commit `.env`, and do not expose Streamlit publicly without authentication. For production, use Microsoft Entra ID, least privilege, durable audit storage, evaluation/monitoring, and server-side approvals.

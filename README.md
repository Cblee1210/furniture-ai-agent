# Furniture AI Agent Center — Interview V1.2.1 Hotfix

V1.2 keeps the full multi-agent UI and upgrades the public Sales Agent demo.

## V1.2 improvements
- Visible cloud backend health status
- Agent execution pipeline: Intent → Product → Quotation → Trade & Logistics → Human Approval
- Sample vs Bulk Order recognition
- Delivered-price quotation decomposition
- EXW is explicitly separated from Freight / Duty & VAT / Last-mile / Final DDP
- Unknown live logistics and tax data are marked pending verification rather than fabricated
- Customer reply draft reflects the selected Incoterm and destination
- Existing bilingual UI, roles/RBAC, CNY/USD/EUR FX, and other agents retained
- FastAPI backend remains deployable on Render Free

## Runtime truthfulness
Current V1.2 is a real public front-end/back-end tool workflow with deterministic intent parsing and business tools. It is LLM-ready, but it does not claim live LLM reasoning until an LLM integration is enabled.

## Deploy
Upload the changed files to the same GitHub repository. Render can redeploy automatically from `main`.


## V1.2.1 hotfix
- Fixes the Trade & Logistics tool import compatibility issue that caused the V1.2 Render startup failure.

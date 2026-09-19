# Furniture AI Agent Center — Full V1.1 Deployment

## Full front-end retained
- 中文 / EN
- 企业员工 / 海外代理商 role selector
- Sales Agent
- Quotation Agent
- Trade & Logistics Agent
- Customer Follow-up Agent
- Product Knowledge Agent
- Marketing & SEO roadmap
- Management Insight roadmap
- CNY / USD / EUR quotation
- Live CNY→USD / EUR FX and rate date
- RBAC / internal-cost hiding
- Agent orchestration
- Human-in-the-loop

## V1.1 upgrade
Sales Agent now calls the FastAPI backend:
Sales → Product Knowledge Tool → Quotation Tool → Trade & Logistics Tool → Human Approval.

## GitHub Pages
Upload `index.html` to repository root. Keep Pages on:
`main` + `/(root)`.

## Render
This repository includes `render.yaml`.
Connect the same GitHub repository to Render and deploy the web service.

Backend:
- Root directory: `backend`
- Build: `pip install -r requirements.txt`
- Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

Optional environment variables:
- `OPENAI_API_KEY`
- `OPENAI_MODEL=gpt-5-mini`

Without an API key, the backend still runs using deterministic fallback.

## Connect frontend to Render
After Render gives an HTTPS URL, open `index.html` and set:

`window.AGENT_API_BASE = "https://YOUR-SERVICE.onrender.com";`

Commit it to GitHub. The Sales Agent will then work for interviewers from the public GitHub Pages URL.

Never put `OPENAI_API_KEY` into `index.html`.

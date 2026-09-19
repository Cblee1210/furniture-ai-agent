# Furniture AI Agent V1.3 — Dual LLM Gateway

## What changed
- Global mode: OpenAI
- China mode: Qwen via Alibaba Cloud Model Studio
- Front-end provider switcher
- LLM intent extraction + LLM customer reply generation
- Product / quotation / trade logic remains deterministic
- Human approval remains mandatory for final commercial commitments
- Automatic deterministic fallback if the selected LLM is unavailable

## Render environment variables

### Common
- `LLM_PROVIDER=openai` (default provider)
- `ALLOW_PROVIDER_OVERRIDE=true` (allows the demo UI to switch OpenAI/Qwen)

### Global / OpenAI
- `OPENAI_API_KEY=...`
- `OPENAI_MODEL=gpt-5-mini`

### China / Qwen
- `DASHSCOPE_API_KEY=...`
- `QWEN_MODEL=qwen3.8-flash`
- `QWEN_BASE_URL=https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

Replace `{WorkspaceId}` with the actual Alibaba Cloud Model Studio workspace ID. The API key and base URL must belong to the same region.

## Deployment
1. Upload/replace repository files in GitHub.
2. In Render, add the environment variables above. Never put API keys in GitHub or `index.html`.
3. Redeploy the service.
4. Verify `/health?provider=openai` and `/health?provider=qwen`.
5. Open GitHub Pages, choose `Global · OpenAI` or `China · Qwen`, then run the Sales Agent.

## Expected runtime indicator
A successful LLM run shows:
- `Intent: llm`
- `Reply: llm`
- `Fallback: none`

If a key/provider is missing or a model call fails, the workflow still runs with deterministic fallback and clearly labels the fallback in the UI.

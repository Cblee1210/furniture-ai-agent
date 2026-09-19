# V1.3.2 China-first deployment

Current interview runtime: China / Qwen. Global OpenAI remains a provider in the LLM Gateway but is not selectable by browser users.

## Render environment variables

- `DEPLOYMENT_REGION=china`
- `DASHSCOPE_API_KEY=<paste in Render only>`
- `QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1`
- `QWEN_MODEL=qwen3.8-max`

Never commit API keys to GitHub or expose them in frontend JavaScript.

## Expected /health

The response should show version `1.3.2`, region `china`, provider `qwen`, model `qwen3.8-max`, and configured `true`.

## Expected Sales Agent runtime

For a successful Qwen call, the UI runtime section should show LLM sources rather than rule fallback. Business facts such as price, freight, duty/VAT, HS classification, and binding terms remain tool/verification/HITL controlled.

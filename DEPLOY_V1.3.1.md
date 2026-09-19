# V1.3.1 Region-Locked Deployment

One codebase, two deployment profiles. The browser cannot select or override the LLM provider.

## Global deployment
Set `DEPLOYMENT_REGION=global`. Configure `OPENAI_API_KEY` and `OPENAI_MODEL`. Requests are locked to OpenAI.

## China deployment
Set `DEPLOYMENT_REGION=china`. Configure `DASHSCOPE_API_KEY`, `QWEN_BASE_URL`, and `QWEN_MODEL`. Requests are locked to Qwen. Do not configure an OpenAI key on the China service.

## UI
The provider dropdown has been removed. `/health` reports the deployment profile and the frontend displays `Global · OpenAI Only` or `China · Qwen Only`.

## Safety boundary
Product, quotation, trade/logistics and human approval remain deterministic business tools. LLM failures fall back to the deterministic workflow.

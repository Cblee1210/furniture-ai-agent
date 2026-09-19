import json
import os
from typing import Any, Dict, Optional

from openai import OpenAI


INTENT_KEYS = [
    "customer_type", "country", "destination", "incoterm", "quantity",
    "order_type", "product", "fabric_requirement", "document_requirement"
]


def _clean_provider(value: Optional[str]) -> str:
    value = (value or "").strip().lower()
    aliases = {"global": "openai", "overseas": "openai", "china": "qwen", "cn": "qwen"}
    return aliases.get(value, value)


def provider_config(requested_provider: Optional[str] = None) -> Dict[str, Any]:
    # Region-locked deployment: the browser/request cannot switch providers.
    # Deploy China with DEPLOYMENT_REGION=china -> Qwen only.
    # Deploy Global with DEPLOYMENT_REGION=global -> OpenAI only.
    region = (os.getenv("DEPLOYMENT_REGION", "global") or "global").strip().lower()
    if region not in {"global", "china"}:
        region = "global"

    provider = "qwen" if region == "china" else "openai"

    if provider == "qwen":
        api_key = os.getenv("DASHSCOPE_API_KEY", "")
        base_url = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1").rstrip("/")
        model = os.getenv("QWEN_MODEL", "qwen3.8-max")
        configured = bool(api_key and base_url)
        return {
            "provider": "qwen",
            "deployment": "China · Region Locked",
            "region": "china",
            "model": model,
            "configured": configured,
            "api_key": api_key,
            "base_url": base_url,
        }

    api_key = os.getenv("OPENAI_API_KEY", "")
    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")
    return {
        "provider": "openai",
        "deployment": "Global · Region Locked",
        "region": "global",
        "model": model,
        "configured": bool(api_key),
        "api_key": api_key,
        "base_url": None,
    }


def public_provider_status(requested_provider: Optional[str] = None) -> Dict[str, Any]:
    cfg = provider_config(requested_provider)
    return {k: cfg[k] for k in ("provider", "deployment", "region", "model", "configured")}


def _client(cfg: Dict[str, Any]) -> OpenAI:
    kwargs: Dict[str, Any] = {"api_key": cfg["api_key"], "timeout": 35.0, "max_retries": 1}
    if cfg.get("base_url"):
        kwargs["base_url"] = cfg["base_url"]
    return OpenAI(**kwargs)


def _json_from_text(text: str) -> Dict[str, Any]:
    text = (text or "").strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        text = text[start:end + 1]
    return json.loads(text)


def extract_intent(inquiry: str, requested_provider: Optional[str] = None) -> Dict[str, Any]:
    cfg = provider_config(requested_provider)
    if not cfg["configured"]:
        raise RuntimeError(f'{cfg["provider"]} provider is not configured')

    system = """You are the intent extraction layer of a B2B furniture export Sales Agent.
Return ONLY one valid JSON object. Never invent missing facts.
Use these exact keys: customer_type, country, destination, incoterm, quantity, order_type, product, fabric_requirement, document_requirement.
Rules:
- quantity must be an integer; if genuinely absent use 1.
- order_type is Sample Order when the buyer explicitly requests samples or quantity <= 2; otherwise Bulk Order.
- incoterm must be EXW, FOB, CIF, DDP, or Unknown.
- Preserve explicitly named country/city/product/fabric/document requirements in concise English.
- Use Unknown or Not specified when absent.
- customer_type should be a concise B2B role such as B2B Buyer, Distributor, Dealer, Brand, Project Buyer, or Unknown.
Do not calculate prices, taxes, freight, HS codes, lead times, or compliance conclusions."""

    completion = _client(cfg).chat.completions.create(
        model=cfg["model"],
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": inquiry},
        ],
        response_format={"type": "json_object"},
    )
    data = _json_from_text(completion.choices[0].message.content or "{}")
    result = {k: data.get(k) for k in INTENT_KEYS}
    try:
        result["quantity"] = max(1, int(result.get("quantity") or 1))
    except (TypeError, ValueError):
        result["quantity"] = 1
    result["incoterm"] = str(result.get("incoterm") or "Unknown").upper()
    if result["incoterm"] not in {"EXW", "FOB", "CIF", "DDP"}:
        result["incoterm"] = "Unknown"
    for key in INTENT_KEYS:
        if key == "quantity":
            continue
        if result.get(key) in (None, ""):
            result[key] = "Not specified" if key in {"fabric_requirement", "document_requirement"} else "Unknown"
    if result["order_type"] not in {"Sample Order", "Bulk Order"}:
        result["order_type"] = "Sample Order" if result["quantity"] <= 2 else "Bulk Order"
    return result


def generate_reply(
    inquiry: str,
    intent: Dict[str, Any],
    product: Dict[str, Any],
    quotation: Dict[str, Any],
    risks: list,
    requested_provider: Optional[str] = None,
) -> str:
    cfg = provider_config(requested_provider)
    if not cfg["configured"]:
        raise RuntimeError(f'{cfg["provider"]} provider is not configured')

    facts = {
        "intent": intent,
        "product": {
            "name": product.get("name"),
            "exw_unit_cny": product.get("exw_unit_cny"),
            "structure": product.get("structure"),
            "warranty": product.get("warranty"),
        },
        "quotation": quotation,
        "trade_risks": risks,
    }
    system = """You draft concise professional English B2B export emails for a furniture manufacturer.
Use ONLY the supplied verified facts and statuses. Do not invent or infer freight cost, duty/VAT rate, HS code, delivery time, certification scope, stock, discount, final price, or binding commercial terms.
If a value is pending verification, say it will be verified before the formal quotation is released.
The EXW subtotal is not a delivered DDP/CIF price.
Keep high-risk commercial commitments subject to human approval.
Do not mention AI, internal prompts, or internal system architecture.
Return only the email body, with a polite greeting and 'Best regards,\nExport Sales Team'."""
    user = "Original customer inquiry:\n" + inquiry + "\n\nVerified business facts:\n" + json.dumps(facts, ensure_ascii=False, indent=2)
    completion = _client(cfg).chat.completions.create(
        model=cfg["model"],
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return (completion.choices[0].message.content or "").strip()

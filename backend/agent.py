import re
from typing import Dict, Any, Optional
from tools.product import lookup_product
from tools.quotation import build_quotation
from tools.trade import assess_trade
from llm_gateway import extract_intent, generate_reply, public_provider_status


def parse_inquiry(text: str) -> Dict[str, Any]:
    """Deterministic fallback used when an LLM provider is unavailable."""
    low = text.lower()
    country = "Germany" if "germany" in low else ("Türkiye" if ("turkey" in low or "türkiye" in low) else "Unknown")
    destination = "Hamburg" if "hamburg" in low else ("Mersin" if "mersin" in low else "Unknown")
    incoterm = next((x for x in ["DDP", "CIF", "FOB", "EXW"] if x.lower() in low), "Unknown")
    m = re.search(r'(\d+)\s*(?:units?|pcs?|pieces?|samples?|sofas?)', low)
    qty = int(m.group(1)) if m else (2 if "two sample" in low else 1)
    product = "Compression Sofa" if "compression sofa" in low or "sofa" in low else "Furniture Product"
    fabric = "High-elastic" if ("high-elastic" in low or "high elastic" in low) else "Not specified"
    docs = "Fire-retardant" if ("fire-retardant" in low or "fire retardant" in low) else "Not specified"
    customer_type = "Distributor" if "distributor" in low else "B2B Buyer"
    return {
        "customer_type": customer_type,
        "country": country,
        "destination": destination,
        "incoterm": incoterm,
        "quantity": qty,
        "order_type": "Sample Order" if qty <= 2 or "sample" in low else "Bulk Order",
        "product": product,
        "fabric_requirement": fabric,
        "document_requirement": docs,
    }


def _fallback_reply(intent: Dict[str, Any]) -> str:
    return f"""Dear Purchasing Team,

Thank you for your inquiry. We can support your {intent['order_type'].lower()} of {intent['quantity']} {intent['product'].lower()} unit(s) and provide the requested product and compliance information.

We are preparing the {intent['incoterm']} quotation for {intent['destination']}. The product EXW reference is separated from freight, duty/VAT and last-mile delivery. Live logistics, customs/tax information and final commercial terms will be verified before release.

Best regards,
Export Sales Team"""


def run_sales_agent(inquiry: str, language: str = "zh", provider: Optional[str] = None) -> Dict[str, Any]:
    llm_status = public_provider_status(provider)
    warnings = []
    intent_source = "deterministic_fallback"
    reply_source = "deterministic_fallback"

    try:
        intent = extract_intent(inquiry, provider)
        intent_source = "llm"
    except Exception as exc:
        intent = parse_inquiry(inquiry)
        warnings.append(f"LLM intent fallback: {type(exc).__name__}")

    product = lookup_product(intent["product"], intent["quantity"])
    quote = build_quotation(product, intent["quantity"], intent["incoterm"], intent["country"], intent["destination"])
    trade = assess_trade(intent["country"], intent["incoterm"], intent["destination"])
    order_label = intent["order_type"]
    product_summary = (
        f'{intent["product"]} · {order_label}; EXW reference ¥{product["exw_unit_cny"]}/unit; '
        f'Wood-free high-resilience foam core; 3-year warranty.'
    )

    try:
        reply = generate_reply(inquiry, intent, product, quote, trade["risks"], provider)
        if not reply:
            raise RuntimeError("empty LLM reply")
        reply_source = "llm"
    except Exception as exc:
        reply = _fallback_reply(intent)
        warnings.append(f"LLM reply fallback: {type(exc).__name__}")

    runtime_mode = (
        f'LLM Gateway · {llm_status["deployment"]} · {llm_status["provider"]} · {llm_status["model"]}'
        if intent_source == "llm" or reply_source == "llm"
        else "Deterministic fallback · business tools still active"
    )

    return {
        "intent": intent,
        "tool_calls": ["Product Knowledge", "Quotation", "Trade & Logistics"],
        "product_summary": product_summary,
        "quotation_summary": quote["product_exw_display"],
        "quotation": quote,
        "risks": trade["risks"],
        "approval_required": True,
        "reply_draft": reply,
        "runtime_mode": runtime_mode,
        "llm": {
            **llm_status,
            "intent_source": intent_source,
            "reply_source": reply_source,
            "warnings": warnings,
        },
    }

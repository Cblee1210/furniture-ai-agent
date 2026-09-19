import os, json, re
from pathlib import Path
from tools.product import search_product
from tools.quotation import calculate_quote
from tools.trade import check_trade_risk

DATA = Path(__file__).parent / "data"

def rule_intent(text: str):
    low=text.lower()
    qty=None
    m=re.search(r"\b(\d+)\s*(?:pcs?|pieces?|samples?|sofas?|units?)\b", low)
    if m: qty=int(m.group(1))
    term=next((x.upper() for x in ["ddp","cif","fob","exw"] if x in low), None)
    country="Türkiye" if ("türkiye" in low or "turkey" in low) else ("Germany" if "germany" in low else None)
    destination="Mersin" if "mersin" in low else ("Hamburg" if "hamburg" in low else None)
    return {
        "customer_type":"B2B Buyer",
        "country":country,
        "product":"Compression Sofa" if "sofa" in low else None,
        "quantity":qty,
        "incoterm":term,
        "destination":destination,
        "fabric_requirement":"High-elastic" if "elastic" in low else None,
        "document_requirement":"Fire-retardant" if "fire" in low else None,
    }

def llm_intent(text: str):
    # Optional production-like path. If OPENAI_API_KEY is absent, the PoC still runs
    # using deterministic extraction. This avoids exposing secrets in the browser.
    key=os.getenv("OPENAI_API_KEY")
    if not key:
        return rule_intent(text), "deterministic-fallback"
    try:
        from openai import OpenAI
        client=OpenAI(api_key=key)
        schema="""Return JSON only with keys:
customer_type,country,product,quantity,incoterm,destination,
fabric_requirement,document_requirement."""
        r=client.responses.create(
            model=os.getenv("OPENAI_MODEL","gpt-5-mini"),
            input=[{"role":"system","content":schema},
                   {"role":"user","content":text}]
        )
        raw=r.output_text.strip()
        raw=re.sub(r"^```json|```$","",raw,flags=re.I|re.M).strip()
        return json.loads(raw), "llm"
    except Exception:
        return rule_intent(text), "deterministic-fallback"

def run_sales_agent(inquiry: str, language="zh"):
    intent, mode=llm_intent(inquiry)
    product=search_product(intent.get("product") or "compression sofa")
    calls=["Product Knowledge"]
    quote=None
    if intent.get("quantity"):
        quote=calculate_quote(
            exw_rmb=product.get("exw_rmb",1260),
            quantity=int(intent["quantity"]),
            incoterm=intent.get("incoterm") or "EXW",
            logistics_rmb=1266 if (intent.get("incoterm") or "").upper()=="CIF" else None,
        )
        calls.append("Quotation")
    risks=check_trade_risk(intent)
    calls.append("Trade & Logistics")
    if language=="zh":
        product_summary=f'{product["name"]}；EXW ¥{product["exw_rmb"]}/件；{product["structure"]}；质保 {product["warranty"]}'
        qsummary=(f'人民币参考小计 ¥{quote["subtotal_rmb"]:.2f}；当前为内部测算，最终商业报价需审批。'
                  if quote else "缺少数量，暂不生成报价。")
    else:
        product_summary=f'{product["name"]}; EXW RMB {product["exw_rmb"]}/unit; {product["structure"]}; warranty {product["warranty"]}'
        qsummary=(f'Indicative CNY subtotal RMB {quote["subtotal_rmb"]:.2f}; final commercial quote requires approval.'
                  if quote else "Quantity missing; quotation not generated.")
    reply=f"""Dear Purchasing Team,

Thank you for your inquiry. We can support the requested compression-sofa sample/order and provide the applicable product and compliance information.

We are preparing the {intent.get("incoterm") or "requested"} quotation for {intent.get("destination") or intent.get("country") or "your destination"}. Before final confirmation, any live freight, customs/tax information and binding commercial terms will be verified and approved by our sales team.

Best regards,
Export Sales Team"""
    return {
        "mode":mode, "intent":intent, "tool_calls":calls,
        "product_summary":product_summary,
        "quotation_summary":qsummary,
        "risks":risks, "approval_required":True,
        "reply_draft":reply
    }

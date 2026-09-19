from typing import Dict, Any

def build_quotation(product: Dict[str, Any], quantity: int, incoterm: str, country: str, destination: str) -> Dict[str, Any]:
    unit = float(product.get("exw_unit_cny", 1260))
    subtotal = unit * quantity
    return {
        "currency":"CNY",
        "unit_exw_cny":unit,
        "product_exw_subtotal_cny":subtotal,
        "product_exw_display":f"¥{subtotal:,.0f} ({quantity} × ¥{unit:,.0f})",
        "freight_status":"Pending live logistics verification",
        "duty_vat_status":"Pending authoritative customs/tax verification",
        "last_mile_status":"Pending destination delivery verification",
        "final_ddp_status":"Pending human approval" if incoterm=="DDP" else "Pending human approval",
        "note":"EXW subtotal is not the final delivered price."
    }

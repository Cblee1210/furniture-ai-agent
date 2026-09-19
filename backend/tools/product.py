from typing import Dict, Any

def lookup_product(product_name: str, quantity: int=1) -> Dict[str, Any]:
    return {
        "name": product_name,
        "exw_unit_cny":1260,
        "structure":"Wood-free high-resilience foam core",
        "warranty":"3 years",
        "order_type":"Sample Order" if quantity <= 2 else "Bulk Order"
    }

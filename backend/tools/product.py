PRODUCTS=[
 {"sku":"SAMPLE-001","name":"Compression Sofa Sample","keywords":["compression sofa","sofa","sample"],
  "exw_rmb":1260,"structure":"Wood-free high-resilience foam core","fabric":"High-elastic fabric available",
  "warranty":"3 years","recovery":"24–72h","carton":"50×50×100 cm","gross_weight":"31 kg"},
 {"sku":"MOD-001","name":"Modular Compression Sofa","keywords":["modular","compression sofa"],
  "exw_rmb":2009,"structure":"Wood-free high-resilience foam core","fabric":"Chenille / customizable",
  "warranty":"3 years","recovery":"24–72h","carton":"Factory confirmation","gross_weight":"Factory confirmation"}
]
def search_product(query):
    q=(query or "").lower()
    for p in PRODUCTS:
        if any(k in q or q in k for k in p["keywords"]):
            return p
    return PRODUCTS[0]

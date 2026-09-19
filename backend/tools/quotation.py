def calculate_quote(exw_rmb, quantity, incoterm="EXW", logistics_rmb=None):
    goods=float(exw_rmb)*int(quantity)
    term=(incoterm or "EXW").upper()
    logistics=0.0 if term=="EXW" else float(logistics_rmb or 0)
    return {"goods_rmb":goods,"logistics_rmb":logistics,"subtotal_rmb":goods+logistics,
            "incoterm":term,"approval_required":True}

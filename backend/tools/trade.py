def check_trade_risk(intent):
    risks=[]
    term=(intent.get("incoterm") or "").upper()
    country=intent.get("country")
    if term in ("CIF","DDP"):
        risks.append("Verify consignee/importer identity and customs-clearance capability.")
    if term=="DDP":
        risks.append("Verify current duty/VAT, importer-of-record arrangement and last-mile delivery constraints.")
    if country:
        risks.append(f"HS classification and destination-country tax rules for {country} require authoritative verification.")
    else:
        risks.append("Destination country is missing.")
    risks.append("Final price, discount, freight commitment and contract terms require human approval.")
    return risks

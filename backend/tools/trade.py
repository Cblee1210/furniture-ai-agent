def check_trade_risk(intent):
    risks = []
    term = (intent.get("incoterm") or "").upper()
    country = intent.get("country")
    destination = intent.get("destination")
    if term in ("CIF", "DDP"):
        risks.append("Verify consignee/importer identity and customs-clearance capability.")
    if term == "DDP":
        risks.append("Verify current duty/VAT, importer-of-record arrangement and last-mile delivery constraints.")
    if country and country != "Unknown":
        risks.append(f"HS classification and destination-country tax rules for {country} require authoritative verification.")
    else:
        risks.append("Destination country is missing or unconfirmed.")
    if destination and destination != "Unknown":
        risks.append(f"Live freight and destination delivery conditions for {destination} require logistics verification.")
    risks.append("Final price, discount, freight commitment and contract terms require human approval.")
    return risks


def assess_trade(country: str, incoterm: str, destination: str):
    return {"risks": check_trade_risk({
        "country": country,
        "incoterm": incoterm,
        "destination": destination,
    })}

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


def assess_trade(country: str, incoterm: str, destination: str):
    """V1.2 compatibility wrapper used by the Sales Agent orchestrator."""
    try:
        result = check_trade_risk(country, incoterm, destination)
        if isinstance(result, dict):
            return result
        if isinstance(result, list):
            return {"risks": result}
        return {"risks": [str(result)]}
    except TypeError:
        # Compatibility with the older check_trade_risk signature.
        try:
            result = check_trade_risk(country, incoterm)
            if isinstance(result, dict):
                return result
            if isinstance(result, list):
                return {"risks": result}
            return {"risks": [str(result)]}
        except TypeError:
            return {"risks": [
                "Verify consignee/importer identity and customs-clearance capability.",
                f"Verify current duty/VAT and importer-of-record requirements for {country}.",
                "HS classification and destination-country tax rules require authoritative verification.",
                "Final price, freight commitment and contract terms require human approval."
            ]}

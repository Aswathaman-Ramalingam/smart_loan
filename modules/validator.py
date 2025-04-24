def validate_fields(fields):
    results = {}
    for key, value in fields.items():
        if value == "Not found":
            results[key] = "Missing"
        elif key in ["Income", "Loan Amount"]:
            results[key] = "Valid" if value.replace(",", "").isdigit() else "Invalid"
        else:
            results[key] = "Valid"
    return results

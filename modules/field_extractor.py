import re

def extract_fields(text: str) -> dict:
    fields = {}

    # Patterns for each field
    patterns = {
        "Name": r"Name[:\s]*([A-Za-z\s]+)",
        "PAN": r"[A-Z]{5}[0-9]{4}[A-Z]",
        "Loan Amount": r"Loan Amount[:\s]*([\d,]+)",
        "IFSC": r"[A-Z]{4}0[A-Z0-9]{6}"
    }

    for field, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            value = match.group(1) if field != "PAN" and field != "IFSC" else match.group(0)
            fields[field] = value.strip().replace(",", "")
        else:
            fields[field] = None

    return fields

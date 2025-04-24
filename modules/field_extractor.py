import re

def extract_fields(ocr_text):
    fields = {
        "Name": "Not found",
        "Address": "Not found",
        "Income": "Not found",
        "Loan Amount": "Not found",
        "ID Number": "Not found"
    }

    # Patterns with labels
    name_pattern = r"(?i)(name|full\s*name):?\s*([A-Za-z\s\.]+)"
    address_pattern = r"(?i)(address|residence|house\s*no|residential\s*address):?\s*([\w\s,\.\-\/]+)"
    income_pattern = r"(?i)(income|salary|annual\s*income|net\s*income):?\s*(\d[\d,\.]*)"
    loan_amount_pattern = r"(?i)(loan\s*amount|loan\s*disbursed):?\s*(\d[\d,\.]*)"
    id_pattern = r"(?i)(id|pan|aadhar|aadhaar|card\s*number):?\s*([A-Z0-9]{10,16})"
    
    # Patterns for standalone fields (without labels)
    standalone_name = r"(?<!\w)([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})(?!\w)"
    standalone_address = r"(?<!\w)(\d+\s+[\w\s,\.\-\/]+(?:Road|Street|Avenue|Lane|Block|Sector|Floor|Area),?\s+[\w\s,\.\-\/]+)(?!\w)"
    standalone_amount = r"(?<!\w)(?:Rs\.?|INR)?\s*(\d{1,3}(?:,\d{3})+|\d{5,})(?!\w)"
    standalone_id = r"(?<!\w)([A-Z0-9]{5,6}[0-9]{4}[A-Z0-9]|[0-9]{12})(?!\w)"
    
    # Name extraction: First try patterns with labels
    name_match = re.search(name_pattern, ocr_text)
    if name_match:
        fields["Name"] = name_match.group(2).strip()
    else:
        # Try without label (for standalone names)
        name_match = re.search(standalone_name, ocr_text)
        if name_match:
            fields["Name"] = name_match.group(1).strip()
    
    # Address extraction: First try patterns with labels
    address_match = re.search(address_pattern, ocr_text)
    if address_match:
        fields["Address"] = address_match.group(2).strip()
    else:
        # Try without label (for standalone addresses)
        address_match = re.search(standalone_address, ocr_text)
        if address_match:
            fields["Address"] = address_match.group(1).strip()
    
    # Income extraction: Check for "Income" related terms
    income_match = re.search(income_pattern, ocr_text)
    if income_match:
        fields["Income"] = income_match.group(2).strip()
    else:
        # Use standalone amount matching if income isn't explicitly labeled
        if "salary" in ocr_text.lower() or "income" in ocr_text.lower() or "statement" in ocr_text.lower():
            amount_match = re.search(standalone_amount, ocr_text)
            if amount_match:
                fields["Income"] = amount_match.group(1).strip()
    
    # Loan amount extraction: Check for loan-related terms
    loan_match = re.search(loan_amount_pattern, ocr_text)
    if loan_match:
        fields["Loan Amount"] = loan_match.group(2).strip()
    else:
        # For loan amounts without a label, check for context or multiple amounts
        if "loan" in ocr_text.lower() or "borrow" in ocr_text.lower():
            amount_match = re.findall(standalone_amount, ocr_text)
            if amount_match and len(amount_match) > 1:  # Take the second one if multiple amounts are found
                fields["Loan Amount"] = amount_match[1].strip()
    
    # ID extraction: Look for ID-related terms
    id_match = re.search(id_pattern, ocr_text)
    if id_match:
        fields["ID Number"] = id_match.group(2).strip()
    else:
        id_match = re.search(standalone_id, ocr_text)
        if id_match:
            fields["ID Number"] = id_match.group(1).strip()
    
    return fields

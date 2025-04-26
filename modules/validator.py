import re

def regex_validate(extracted_data, template_name):
    validations = {}

    if template_name == "PAN Card":
        validations["Name"] = bool(re.match(r"^[A-Za-z ]{3,}$", extracted_data.get("Name", "").strip()))
        
        validations["ID"] = bool(re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$", extracted_data.get("ID", "").strip()))
    
    elif template_name == "Aadhaar Card":
        validations["Name"] = bool(re.match(r"^[A-Za-z ]{3,}$", extracted_data.get("Name", "").strip()))
        validations["ID"] = bool(extracted_data.get("ID", "").isdigit() and len(extracted_data.get("ID", "").strip()) == 12)
        if len(extracted_data.get("Address"))>10:
            validations["Address"] = True
        elif len(extracted_data.get("Address"))==0:
            validations["Address"] = None
        else:
            validations["Address"] = False

    elif template_name == "Bank Statement":
        validations["Name"] = bool(re.match(r"^[A-Za-z ]{3,}$", extracted_data.get("Name", "").strip()))
        if len(extracted_data.get("Address"))>10:
            validations["Address"] = True
        elif len(extracted_data.get("Address"))==0:
            validations["Address"] = None
        else:
            validations["Address"] = False

        validations["Withdrawals"] = bool(re.match(r"^\d+$", extracted_data.get("Withdrawals", "").strip()))
    
    return validations

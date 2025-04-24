import pytesseract
from .preprocessor import preprocess_image

def extract_text(image_path):
    processed = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed)
    return text, processed

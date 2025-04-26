import pytesseract
import numpy as np
import cv2
from PIL import Image

def extract_data_using_template(pil_image, template):
    open_cv_image = np.array(pil_image)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

    extracted_data = {}
    for field, coords in template.items():
        x, y, w, h = coords
        cropped = open_cv_image[y:y+h, x:x+w]

        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(thresh, config=custom_config)
        extracted_text = text.strip().replace("\n", " ")
        extracted_data[field] = extracted_text

    return extracted_data

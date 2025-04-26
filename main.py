import streamlit as st
from PIL import Image
import os
import json
from modules.ocr_engine import extract_text_from_image
from modules.preprocessor import extract_data_using_template
from modules.validator import regex_validate

TEMPLATES = {
    "Aadhaar Card": {
        "Name": (150, 150, 400, 30),
        "ID": (150, 300, 400, 50),
        "Address": (400, 350, 600, 10),
    },
    "Bank Statement": {
        "Name": (50, 100, 300, 30),
        "Address": (50, 120, 300, 60),
        "Withdrawals": (300, 475, 200, 50),
    },
    "PAN Card": {
        "Name": (12, 80, 200, 50),
        "ID": (10, 220, 400, 60),
    }
}

st.title("Document Data Extraction Tool")

mode = st.radio("Select Mode", ["Test Images", "Upload Image"])

image = None

if mode == "Test Images":
    test_images = {
        "Aadhaar Card": "images/aadhar_card.jpg",
        "Bank Statement": "images/bank_statement.png",
        "PAN Card": "images/pan_card.jpg"
    }
    choice = st.selectbox("Choose Template", list(test_images.keys()))
    image_path = test_images[choice]
    image = Image.open(image_path)

else:
    choice = st.selectbox("Choose Template for Uploaded Image", list(TEMPLATES.keys()))
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

if image is not None:
    st.image(image, caption="Selected Document", use_container_width=True)

    text = extract_text_from_image(image)
    extracted_data = extract_data_using_template(image, TEMPLATES[choice])

    st.subheader("Extracted Fields (Editable)")
    edited_data = {}
    for key, value in extracted_data.items():
        edited_value = st.text_input(f"{key}", value)
        edited_data[key] = edited_value

    st.subheader("Regex Validation")
    validation = regex_validate(edited_data, choice)
    st.json(validation)

    st.subheader("Save Extracted Data")
    filename = st.text_input("Save As (Enter filename without extension):", value=edited_data.get("Name", "document").replace(" ", "_"))
    if st.button("Save JSON"):
        if filename:
            os.makedirs("saved_data", exist_ok=True)
            save_path = f"saved_data/{filename}.json"
            with open(save_path, "w") as f:
                json.dump(edited_data, f, indent=4)
            st.success(f"Data saved successfully as {save_path}")
        else:
            st.error("Filename cannot be empty.")
else:
    st.info("Please select or upload an image first.")

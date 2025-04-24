import streamlit as st
from config import TEST_IMAGES
from modules import ocr_engine, field_extractor, validator

st.set_page_config(page_title="Smart Loan OCR", layout="wide")
st.title("Smart Personal Loan Document OCR")

# Dropdown to select the test image
st.subheader("Select a Test Image")
selected_image = st.selectbox("Choose a sample image", TEST_IMAGES)

# Upload option
st.subheader("Or, Upload Your Document")
uploaded_file = st.file_uploader("Upload a personal loan document (image)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Save uploaded file temporarily
    with open("uploaded_temp.jpg", "wb") as f:
        f.write(uploaded_file.read())

    st.image("uploaded_temp.jpg", caption="Uploaded Document", use_container_width=True)

    if st.button("Process Uploaded Document"):
        with st.spinner("Running OCR..."):
            extracted_text, _ = ocr_engine.extract_text("uploaded_temp.jpg")
            fields = field_extractor.extract_fields(extracted_text)
            validations = validator.validate_fields(fields)

        st.subheader("Extracted Fields")
        for key in fields:
            st.text(f"{key}: {fields[key]}")

        st.subheader("Validation Results")
        for key in validations:
            st.text(f"{key}: {validations[key]}")

elif selected_image:
    # Show selected test image
    st.image(selected_image, caption=selected_image.split('/')[-1], use_container_width=True)

    if st.button("Process Test Image"):
        with st.spinner("Running OCR..."):
            extracted_text, _ = ocr_engine.extract_text(selected_image)
            fields = field_extractor.extract_fields(extracted_text)
            validations = validator.validate_fields(fields)

        st.subheader("Extracted Fields")
        for key in fields:
            st.text(f"{key}: {fields[key]}")

        st.subheader("Validation Results")
        for key in validations:
            st.text(f"{key}: {validations[key]}")

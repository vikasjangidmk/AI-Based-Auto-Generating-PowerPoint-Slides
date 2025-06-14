import streamlit as st
import requests

# Define FastAPI backend URL
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI PowerPoint Generator", layout="centered")

st.title("📊 AI-Based Auto-Generating PowerPoint Slides")
st.write("Upload documents and generate slides automatically.")

# Upload File
uploaded_file = st.file_uploader("📂 Upload a document (TXT, PDF, DOCX, CSV)", type=["txt", "pdf", "docx", "csv"])

if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' uploaded successfully.")
    
    # Save the file temporarily
    files = {"file": uploaded_file}
    upload_response = requests.post(f"{BASE_URL}/upload/", files=files)

    if upload_response.status_code == 200:
        st.success("✅ File uploaded to server successfully!")
        if st.button("🚀 Generate Slides"):
            generate_response = requests.get(f"{BASE_URL}/generate/")

            if generate_response.status_code == 200:
                st.success("✅ Slides generated successfully!")
                download_url = f"{BASE_URL}/download/?filename=output/generated_presentation.pptx"
                st.markdown(f"[📥 Download PowerPoint](output/generated_presentation.pptx)", unsafe_allow_html=True)
            else:
                st.error("⚠️ Slide generation failed! Check API logs.")
    else:
        st.error("⚠️ File upload failed! Please try again.")


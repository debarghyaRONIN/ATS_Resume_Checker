from dotenv import load_dotenv
import base64
import streamlit as st
import os
import fitz  # PyMuPDF
import logging

from google import genai
from google.genai import types 


# Load environment variables (for local development)
# In Streamlit Cloud, use secrets via st.secrets
load_dotenv()

# Get API key from secrets (Streamlit Cloud) or environment variable (local)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except (KeyError, FileNotFoundError):
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("API Key not found. Please configure GOOGLE_API_KEY in Streamlit secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")


def get_gemini_response(input_text, pdf_content, prompt):
    """Generate response using Gemini API with error handling."""
    try:
        # Decode base64 → bytes
        image_bytes = base64.b64decode(pdf_content[0]["data"])

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(input_text),
                        types.Part.from_bytes(
                            data=image_bytes,
                            mime_type="image/jpeg"
                        ),
                        types.Part.from_text(prompt),
                    ],
                )
            ],
        )

        return response.text
    
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return f" Error processing request: {str(e)}"


@st.cache_data(show_spinner=False)
def input_pdf_setup(uploaded_file):
    """Convert PDF to base64 encoded JPEG image (cached)."""
    try:
        if uploaded_file is None:
            raise FileNotFoundError("No file uploaded")
        
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        # First page → image
        first_page = pdf_document.load_page(0)
        pix = first_page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))  # Better quality

        img_bytes = pix.tobytes("jpeg")

        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_bytes).decode()
        }]

        return pdf_parts
    
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise Exception(f" Error processing PDF: {str(e)}")




input_text = st.text_area("📋 Job Description:", key="input", help="Paste the job description here")
uploaded_file = st.file_uploader("📄 Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.success("✅ PDF Uploaded Successfully")
else:
    st.info("⏳ Please upload a PDF resume to get started")

col1, col2 = st.columns(2)
with col1:
    submit1 = st.button("📝 Tell Me About the Resume", use_container_width=True)
with col2:
    submit2 = st.button("📊 Percentage Match", use_container_width=True)



input_prompt1 = """
You are an experienced Technical Human Resource Manager.
Your task is to review the provided resume against the job description.

Please share your professional evaluation on whether the candidate's profile aligns with the role.

Highlight:
- Strengths
- Weaknesses
- Overall fit
"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner.

Evaluate the resume against the job description and provide:
1. Match Percentage (first line)
2. Missing Keywords
3. Final Thoughts
"""



if submit1:
    # Validate inputs
    if not input_text.strip():
        st.warning("⚠️ Please enter a job description")
    elif uploaded_file is not None:
        with st.spinner("🔄 Analyzing resume..."):
            try:
                pdf_content = input_pdf_setup(uploaded_file)
                response = get_gemini_response(input_text, pdf_content, input_prompt1)
                st.subheader("📋 Analysis")
                st.write(response)
            except Exception as e:
                st.error(f" Error: {str(e)}")
                logger.error(f"Error in submit1: {str(e)}")
    else:
        st.warning("⚠️ Please upload a resume (PDF)")

elif submit2:
    # Validate inputs
    if not input_text.strip():
        st.warning("⚠️ Please enter a job description")
    elif uploaded_file is not None:
        with st.spinner("🔄 Calculating match percentage..."):
            try:
                pdf_content = input_pdf_setup(uploaded_file)
                response = get_gemini_response(input_text, pdf_content, input_prompt2)
                st.subheader("📊 ATS Result")
                st.write(response)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                logger.error(f"Error in submit2: {str(e)}")
    else:
        st.warning("⚠️ Please upload a resume (PDF)")
from dotenv import load_dotenv
import base64
import streamlit as st
import os
import fitz  # PyMuPDF

from google import genai
from google.genai import types  # ✅ REQUIRED for multimodal


load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")



def get_gemini_response(input_text, pdf_content, prompt):
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


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        # First page → image
        first_page = pdf_document.load_page(0)
        pix = first_page.get_pixmap()

        img_bytes = pix.tobytes("jpeg")

        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_bytes).decode()
        }]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")




input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("Percentage Match")



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
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)

       
        response = get_gemini_response(input_text, pdf_content, input_prompt1)

        st.subheader("Analysis")
        st.write(response)
    else:
        st.warning("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)

       
        response = get_gemini_response(input_text, pdf_content, input_prompt2)

        st.subheader("ATS Result")
        st.write(response)
    else:
        st.warning("Please upload the resume")
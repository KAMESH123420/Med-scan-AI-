import io
import streamlit as st
import pymupdf
import pytesseract

from PIL import Image, ImageOps
from google import genai

st.set_page_config(
    page_title="MedScan AI",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 MedScan AI")
st.subheader("AI Medical Report Scanner")

st.write(
    "Upload a medical report and receive an "
    "AI-generated explanation in simple English."
)

st.warning(
    "Educational assistance only. This tool does not "
    "diagnose diseases or replace a doctor."
)


def extract_pdf_text(file_bytes):
    with pymupdf.open(
        stream=file_bytes,
        filetype="pdf"
    ) as document:
        return "\n".join(
            page.get_text()
            for page in document
        )


def extract_image_text(file_bytes):
    image = Image.open(io.BytesIO(file_bytes))
    image = ImageOps.grayscale(image)

    return pytesseract.image_to_string(
        image,
        lang="eng"
    )


uploaded_file = st.file_uploader(
    "Upload your medical report",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:
    file_bytes = uploaded_file.getvalue()

    try:
        if uploaded_file.type == "application/pdf":
            extracted_text = extract_pdf_text(file_bytes)
        else:
            extracted_text = extract_image_text(file_bytes)

        if not extracted_text.strip():
            st.warning(
                "No text was detected. The PDF may be scanned "
                "or the image may be unclear."
            )

        else:
            st.subheader("📄 Extracted Report")

            edited_text = st.text_area(
                "Review the extracted text before analysis",
                value=extracted_text,
                height=250
            )

            if st.button("🧠 Analyze with Gemini AI"):
                if not edited_text.strip():
                    st.error("No report text is available.")
                else:
                    try:
                        api_key = st.secrets["GEMINI_API_KEY"]

                        client = genai.Client(
                            api_key=api_key
                        )

                        prompt = f"""
You are a medical-report explanation assistant.

Explain the following report in simple English.

1. Summarize the findings.
2. Explain medical terminology.
3. Identify values explicitly marked outside the
   laboratory's reference ranges.
4. Mention missing or unclear information.
5. Do not invent test results or diagnose diseases.
6. Do not recommend changing medication.
7. Advise the user to discuss concerning findings
   with a qualified healthcare professional.

Report text:
{edited_text}
"""

                        with st.spinner(
                            "Gemini is analyzing your report..."
                        ):
                            response = client.models.generate_content(
                                model="gemini-2.5-flash",
                                contents=prompt
                            )

                        st.subheader("🧠 AI Explanation")
                        st.markdown(response.text)

                    except KeyError:
                        st.error(
                            "GEMINI_API_KEY was not found. "
                            "Check Streamlit App Settings → Secrets."
                        )

                    except Exception as error:
    st.error("AI analysis failed.")
    st.code(str(error)[:1000])

    except Exception:
        st.error(
            "Unable to process this file. Try another report."
        )

st.divider()

st.caption(
    "MedScan AI | For informational purposes only. "
    "Not a substitute for professional medical advice."
)

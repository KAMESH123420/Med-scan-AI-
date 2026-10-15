import streamlit as st
import pymupdf
import io
from PIL import Image

st.set_page_config(
    page_title="MedScan AI",
    page_icon="🏥",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #f4f8fc;
}
h1 {
    color: #123b66;
}
h2, h3 {
    color: #176b87;
}
[data-testid="stFileUploader"] {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #d7e4f0;
}
</style>
""", unsafe_allow_html=True)

st.title("🏥 MedScan AI")
st.subheader("Your AI-powered medical report assistant")

st.write(
    "Upload a medical report to extract its text "
    "and understand the information it contains."
)

st.info(
    "Privacy notice: Use fictional or de-identified reports "
    "while testing this prototype. Do not upload identifiable "
    "patient records to a public repository."
)

uploaded_file = st.file_uploader(
    "Upload your medical report",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:
    file_bytes = uploaded_file.getvalue()

    st.success("File uploaded successfully!")

    if uploaded_file.type == "application/pdf":
        try:
            with pymupdf.open(
                stream=file_bytes,
                filetype="pdf"
            ) as document:
                extracted_text = "\n".join(
                    page.get_text()
                    for page in document
                )

            st.subheader("📄 Extracted Report Text")

            if extracted_text.strip():
                st.text_area(
                    "Report contents",
                    extracted_text,
                    height=300
                )

                st.download_button(
                    "Download Extracted Text",
                    data=extracted_text,
                    file_name="extracted_report.txt",
                    mime="text/plain"
                )

            else:
                st.warning(
                    "No selectable text was found. "
                    "This may be a scanned PDF. OCR support "
                    "will be added in the next development stage."
                )

        except Exception:
            st.error(
                "Unable to read this PDF. "
                "Please try another file."
            )

    else:
        st.subheader("🖼️ Uploaded Report Image")

        try:
            image = Image.open(io.BytesIO(file_bytes))
            st.image(
                image,
                caption="Uploaded medical report",
                use_container_width=True
            )

            st.warning(
                "Image text extraction will be added in "
                "the next development stage."
            )

        except Exception:
            st.error("Unable to open this image.")

st.divider()

st.caption(
    "MedScan AI | Prototype for educational purposes. "
    "Extracted information is not a medical diagnosis."
)

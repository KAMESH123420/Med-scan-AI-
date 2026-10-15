import io
import pymupdf
import pytesseract

from PIL import Image, ImageOps


def extract_pdf_text(file_bytes):
    """Extract selectable text from a PDF."""

    with pymupdf.open(
        stream=file_bytes,
        filetype="pdf"
    ) as document:
        return "\n".join(
            page.get_text()
            for page in document
        )


def extract_image_text(file_bytes):
    """Extract text from an image using OCR."""

    image = Image.open(io.BytesIO(file_bytes))
    image = ImageOps.grayscale(image)

    return pytesseract.image_to_string(
        image,
        lang="eng"
    )

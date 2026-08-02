import fitz
import cv2

from app.services.exceptions import EncodingError


def encode_pdf(document):
    pdf = fitz.open()
    try:
        for page in document:
            success, encoded = cv2.imencode(".png", page.image)
            if not success:
                raise EncodingError("Could not encode PDF page")

            image = fitz.Pixmap(encoded.tobytes())
            pdf_page = pdf.new_page(width=page.width, height=page.height)
            pdf_page.insert_image(pdf_image.rect, pixmap=image)

            return pdf.tobytes()
    finally:
        pdf.close()

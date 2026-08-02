import fitz
import cv2
import numpy as np

from app.media import Page, Document
from app.services.exceptions import ValidationError


def decode_pdf(data):
    try:
        pdf = fitz.open(stream=data, filetype="pdf")
    except Exception:
        raise ValidationError("Invalid PDF")

    pages = []
    for number, pdf_page in enumerate(pdf, start=1):
        matrix = fitz.Matrix(3, 3)
        pixmap = pdf_page.get_pixmap(matrix=matrix, alpha=False)
        image = np.frombuffer(pixmap.samples, dtype=np.uint8)
        image = image.reshape(pixmap.height, pixmap.width, pixmap.n)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        pages.append(Page(image, number, pdf_page.rect.width, pdf_page.rect.height))

    if not pages:
        raise ValidationError("PDF contains no pages")

    pdf.close()

    return Document(pages)

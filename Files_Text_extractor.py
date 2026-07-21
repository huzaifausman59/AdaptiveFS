import pdfplumber
import docx


def extract_pdf_text(pdf_path):
    
    extracted_text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                extracted_text += page_text + "\n"

    return extracted_text


def extract_docx_text(docx_path):
    
    document = docx.Document(docx_path)

    extracted_text = ""

    for paragraph in document.paragraphs:
        extracted_text += paragraph.text + "\n"

    return extracted_text
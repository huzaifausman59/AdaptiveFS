import os
import logging
import pdfplumber
import docx
from PIL import Image
from PIL.ExifTags import TAGS

#*******************logging configuration****************
logging.basicConfig(
    filename="extraction_errors.log",
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def log_extraction_error(error, file_path):
    logging.error(
        f"Error: {type(error).__name__} | Reason: {error} | FileName: {os.path.basename(file_path)}"
    )

#******************PDF extraction function****************

def extract_pdf_text(pdf_path):

    extracted_text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    extracted_text += page_text + "\n"

    except Exception as e:
        print(f"Error reading PDF '{pdf_path}': {e}")
        log_extraction_error(e, pdf_path)
        return ""

    return extracted_text

# ******************Word document extraction function****************

def extract_docx_text(docx_path):

    extracted_text = ""

    try:
        document = docx.Document(docx_path)

        for paragraph in document.paragraphs:
            extracted_text += paragraph.text + "\n"

    except Exception as e:
        print(f"Error reading Word document '{docx_path}': {e}")
        log_extraction_error(e, docx_path)
        return ""

    return extracted_text



#*****************image metadata extraction function****************

def extract_image_metadata(image_path):
    metadata = {}

    try:
        image = Image.open(image_path)

        exif_data = image.getexif()

        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                metadata[tag] = value

    except Exception as e:
        print(f"Error reading image '{image_path}': {e}")
        log_extraction_error(e, image_path)

    return metadata

#*******************text file extraction function****************

def extract_text_file(txt_path):
    try:
        with open(txt_path, "r", encoding="utf-8", errors="ignore") as file:
            text = file.read()

        return text

    except Exception as e:
        log_extraction_error(e, txt_path)
        return None

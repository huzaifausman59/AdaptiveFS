import pdfplumber
import docx
from PIL import Image
from PIL.ExifTags import TAGS

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
        return ""

    return extracted_text


def extract_docx_text(docx_path):
    
    extracted_text = ""

    try:
        document = docx.Document(docx_path)

        for paragraph in document.paragraphs:
            extracted_text += paragraph.text + "\n"

    except Exception as e:
        print(f"Error reading Word document '{docx_path}': {e}")
        return ""

    return extracted_text

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

    return metadata


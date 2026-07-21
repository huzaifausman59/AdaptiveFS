from Files_Text_extractor import extract_pdf_text

pdf_path = r"C:\Users\aliad\Downloads\PDF_sample.pdf"

text = extract_pdf_text(pdf_path)

print(text)
print("********************************************************************************")
from Files_Text_extractor import extract_docx_text

docx_path = r"C:\Users\aliad\Downloads\FYP_features.docx"

text = extract_docx_text(docx_path)

print(text)

from Files_Text_extractor import extract_pdf_text

print(extract_pdf_text("does_not_exist.pdf"))

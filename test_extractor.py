from Files_Text_extractor import extract_pdf_text

pdf_path = r"C:\Users\aliad\Downloads\PDF_sample.pdf"

text = extract_pdf_text(pdf_path)

print(text)
import fitz  # PyMuPDF

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    # To extract text from each page
    for page in doc:
        text += page.get_text()

    doc.close()
    return text

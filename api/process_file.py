import PyPDF2
from api.clean_text import clean_text


def process_file(file):
    filename = file.filename.lower()

    if filename.endswith(".txt"):
        text = file.read().decode("utf-8", errors="ignore")
        cleaned_text = clean_text(text)
        return cleaned_text

    elif filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        cleaned_text = clean_text(page.extract_text() for page in reader.pages)
        return text

    else:
        raise ValueError("Formato de arquivo não suportado")

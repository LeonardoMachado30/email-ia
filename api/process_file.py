import PyPDF2
from api.clean_text import clean_text
from typing import BinaryIO


def process_file(file: BinaryIO) -> str:
    """
    Processa arquivos .txt ou .pdf, extraindo e limpando o texto para uso em IA.

    Objetivo:
    - Ler o conteúdo de arquivos de texto (.txt) ou PDF (.pdf).
    - Limpar e normalizar o texto utilizando a função clean_text.
    - Retornar o texto limpo, pronto para processamento posterior.

    Instruções:
    - Forneça um arquivo com atributo 'filename' e método 'read' (para .txt) ou um arquivo PDF.
    - Apenas arquivos .txt e .pdf são suportados.
    - Em caso de formato não suportado, será levantada uma exceção.

    Parâmetros:
    - file: Objeto de arquivo enviado pelo usuário.

    Retorno:
    - str: Texto limpo extraído do arquivo.
    """
    filename = file.filename.lower()

    if filename.endswith(".txt"):
        text = file.read().decode("utf-8", errors="ignore")
        cleaned_text = clean_text(text)
        return cleaned_text

    elif filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        cleaned_text = clean_text(text)
        return cleaned_text

    else:
        raise ValueError("Formato de arquivo não suportado")

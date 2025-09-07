import re
import unicodedata


def clean_text(text: str) -> str:
    """
    Limpa e normaliza o texto para processamento de IA.

    Objetivo:
    - Remover ruídos, caracteres especiais, emojis, URLs, menções e hashtags.

    Instruções:
    - Passe o texto como string.
    - O método retorna o texto limpo e padronizado.

    Parâmetros:
    - text (str): Texto a ser limpo.

    Retorno:
    - str: Texto limpo.

    Exemplo:
        texto_limpo = clean_text("Olá! 😊 Veja mais em http://exemplo.com #promoção @usuario")
        # Saída: "Ola! Veja mais em"
    """
    text = unicodedata.normalize("NFKD", text)  # Normaliza acentuação
    text = text.encode("ascii", "ignore").decode("ascii")  # Remove acentos

    text = re.sub(r"http\S+|www\S+", "", text)  # Remove URLs

    text = re.sub(r"[#@]\S+", "", text)  # Remove hashtags e menções

    emoji_pattern = re.compile(
        "["
        "\U0001f600-\U0001f64f"  # Emojis emoticons
        "\U0001f300-\U0001f5ff"  # Emojis símbolos e pictogramas
        "\U0001f680-\U0001f6ff"  # Emojis transporte e mapas
        "\U0001f1e0-\U0001f1ff"  # Emojis bandeiras
        "]+",
        flags=re.UNICODE,
    )
    text = emoji_pattern.sub(r"", text)  # Remove emojis

    text = re.sub(r"[\r\n\t]+", " ", text)  # Substitui quebras de linha/tabs por espaço
    text = re.sub(r"\s{2,}", " ", text)  # Reduz múltiplos espaços

    text = "".join(ch for ch in text if ch.isprintable())  # Remove não-imprimíveis

    return text.strip()

from typing import Literal
from api.query import query

API_URL_SUGGESTION = "https://router.huggingface.co/v1/chat/completions"


def gerar_resposta_sugerida(
    texto: str, categoria: Literal["PRODUTIVO", "IMPRODUTIVO"]
) -> str:
    """
    Gera uma resposta automática para e-mails usando IA.

    Objetivo:
    - Criar uma resposta breve e adequada ao contexto do e-mail, conforme a categoria.

    Instruções:
    - Informe o texto do e-mail (str) e a categoria ('PRODUTIVO' ou 'IMPRODUTIVO').
    - PRODUTIVO: resposta cordial e sucinta, apenas agradecendo.
    - IMPRODUTIVO: resposta objetiva, confirmando recebimento e informando processamento.

    Pontos principais:
    - Monta o prompt conforme a categoria.
    - Usa o modelo Llama 3.1-8B-Instruct via API Hugging Face.
    - Retorna a resposta gerada ou mensagem de erro.
    """

    if categoria == "PRODUTIVO":
        prompt = (
            "Você é um assistente de suporte ao cliente. "
            "Sua tarefa é criar uma resposta breve, cordial e profissional para o e-mail abaixo. "
            "Apenas confirme de forma educada que a mensagem foi recebida e que a reunião está confirmada, "
            "sem frases artificiais como 'vamos processar sua mensagem' ou 'gostamos de confirmar'. "
            "A resposta deve soar natural, clara e respeitosa, como se fosse escrita por um humano em um ambiente de trabalho.\n\n"
            f"E-mail: {texto}"
        )
    else:
        prompt = (
            "Você é um assistente cordial. "
            "Sua tarefa é criar uma resposta curta, simples e natural para um e-mail recebido. "
            "A resposta deve soar casual, amigável e espontânea, sem parecer escrita por uma inteligência artificial. "
            "Evite frases robóticas ou formais demais (como 'estarei respondendo em breve' ou 'agradeço desde já'). "
            "Responda apenas de forma gentil e apropriada ao contexto.\n\n"
            f"E-mail: {texto}"
        )

    try:
        resposta = query(
            API_URL_SUGGESTION,
            {
                "messages": [{"role": "user", "content": prompt}],
                "model": "meta-llama/Llama-3.1-8B-Instruct:cerebras",
            },
        )
        if resposta and "choices" in resposta and len(resposta["choices"]) > 0:
            return resposta["choices"][0]["message"]["content"]
        return "Não foi possível gerar a resposta."
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")
        return "Erro ao gerar resposta."

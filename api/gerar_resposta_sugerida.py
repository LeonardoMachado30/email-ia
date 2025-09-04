from api.query import query


API_URL_SUGGESTION = "https://router.huggingface.co/v1/chat/completions"


def gerar_resposta_sugerida(texto, categoria):
    print("\nGERANDO SUGESTÂO DE EMAIL...\n\n")
    prompt = (
        f"Você é um assistente cordial. Sua tarefa é criar uma resposta educada e breve para o e-mail a seguir, agradecendo a mensagem, mas sem sugerir qualquer ação adicional. A resposta deve ser curta e gentil.\n Email: {texto}"
        if categoria == "PRODUTIVO"
        else f"Você é um assistente de suporte ao cliente. Sua tarefa é criar uma resposta breve e profissional para o e-mail a seguir, focando em confirmar o recebimento e informar que o pedido está sendo processado.\n Email: {texto}"
    )

    try:
        resposta = query(
            API_URL_SUGGESTION,
            {
                "messages": [{"role": "user", "content": prompt}],
                "model": "meta-llama/Llama-3.1-8B-Instruct:cerebras",
            },
        )
        if "choices" in resposta and len(resposta["choices"]) > 0:
            print(f"SEGUESTÃO GERADA: {resposta["choices"][0]["message"]["content"]}")
            return resposta["choices"][0]["message"]["content"]
        return "Não foi possível gerar a resposta."
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")
        return "Erro ao gerar resposta."

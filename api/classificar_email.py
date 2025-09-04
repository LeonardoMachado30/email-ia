from transformers import pipeline
from api.clean_text import clean_text

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


def classificar_email(email: str) -> str:
    # Limpeza profunda do texto
    email_limpo = clean_text(email)

    candidate_labels = ["PRODUTIVO", "IMPRODUTIVO"]

    # Hypothesis template enriquecido com exemplos de cada categoria
    hypothesis_template = (
        "Classifique o email como PRODUTIVO se ele estiver relacionado a trabalho/profissional, "
        "exigindo ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema, reuniões, trabalho, empresa, reunião, gestores, funcionarios, pessoa juridica). "
        "Classifique como IMPRODUTIVO se o email for pessoal, sem necessidade de ação profissional imediata (ex.: felicitações, agradecimentos, mensagens pessoais, pessoa fisica). {}"
    )

    try:
        resposta = classifier(
            email_limpo,
            candidate_labels=candidate_labels,
            hypothesis_template=hypothesis_template,
        )

        print("Resposta classificação:", resposta)

        if not resposta or "labels" not in resposta or "scores" not in resposta:
            return "ERRO_CLASSIFICACAO"

        label_scores = dict(zip(resposta["labels"], resposta["scores"]))

        # Retorna a categoria com maior score
        return (
            "PRODUTIVO"
            if label_scores.get("PRODUTIVO", 0) >= label_scores.get("IMPRODUTIVO", 0)
            else "IMPRODUTIVO"
        )

    except Exception as e:
        print(f"Erro na classificação: {e}")
        return "ERRO_CLASSIFICACAO"

from transformers import pipeline
from api.clean_text import clean_text
import torch

# Pipeline mais leve e CPU-friendly
classifier = pipeline(
    "zero-shot-classification",
    model="typeform/distilbert-base-uncased-mnli",  # modelo pequeno
    device=-1,  # CPU
    return_all_scores=False,
    use_fast=True,
    model_kwargs={
        "dtype": torch.float32,
        "low_cpu_mem_usage": True,
    },
)


def classificar_email(email: str) -> str:
    """
    Classifica e-mails em PRODUTIVO ou IMPRODUTIVO.
    PRODUTIVO = relacionado a trabalho/profissional.
    IMPRODUTIVO = pessoal ou sem relação com trabalho.
    """
    email_limpo = clean_text(email)
    print(email_limpo)
    candidate_labels = [
        "E-mail relacionado a trabalho/profissional",
        "E-mail pessoal ou não relacionado a trabalho",
    ]

    hypothesis_template = (
        "Classifique o e-mail como {}. "
        "Use PRODUTIVO apenas para e-mails relacionados a trabalho, projetos, reuniões ou tarefas profissionais. "
        "Use IMPRODIVO para mensagens pessoais, felicitações, cumprimentos, eventos de vida pessoal."
    )

    try:
        resposta = classifier(
            email_limpo,
            candidate_labels=candidate_labels,
            hypothesis_template=hypothesis_template,
        )

        if not resposta or "labels" not in resposta or "scores" not in resposta:
            return "ERRO_CLASSIFICACAO"

        # Retorna "PRODUTIVO" ou "IMPRODUTIVO" conforme a label
        melhor_label = resposta["labels"][0]
        if melhor_label == "E-mail relacionado a trabalho/profissional":
            return "PRODUTIVO"
        elif melhor_label == "E-mail pessoal ou não relacionado a trabalho":
            return "IMPRODUTIVO"
        else:
            return "ERRO_CLASSIFICACAO"

    except Exception as e:
        print(f"Erro na classificação: {e}")
        return "ERRO_CLASSIFICACAO"

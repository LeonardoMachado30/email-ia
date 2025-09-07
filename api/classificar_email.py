from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from api.clean_text import clean_text
import torch

# Estratégias de otimização para ambiente com pouca RAM:
# - Carregar tokenizer e modelo explicitamente e fora do pipeline (evita overhead)
# - Usar modelo ainda menor e mais eficiente se possível
# - Desabilitar cache do HuggingFace (evita uso excessivo de RAM)
# - Evitar prints desnecessários
# - Carregar o pipeline apenas uma vez (singleton)
# - Limitar tamanho do texto de entrada

import os

os.environ["TRANSFORMERS_CACHE"] = "/tmp"  # Evita cache em memória
os.environ["HF_HOME"] = "/tmp"
os.environ["HF_DATASETS_CACHE"] = "/tmp"
os.environ["HF_METRICS_CACHE"] = "/tmp"

# Modelo ainda menor e eficiente (se possível, use um modelo tiny)
MODEL_NAME = "typeform/distilbert-base-uncased-mnli"

# Singleton para pipeline (evita múltiplas cargas)
_classifier = None


def get_classifier():
    global _classifier
    if _classifier is None:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_NAME,
            dtype=torch.float32,
            low_cpu_mem_usage=True,
        )
        _classifier = pipeline(
            "zero-shot-classification",
            model=model,
            tokenizer=tokenizer,
            device=-1,  # CPU
            return_all_scores=False,
            use_fast=True,
        )
    return _classifier


def classificar_email(email: str) -> str:
    """
    Classifica e-mails em PRODUTIVO ou IMPRODUTIVO.
    PRODUTIVO = relacionado a trabalho/profissional.
    IMPRODUTIVO = pessoal ou sem relação com trabalho.
    """
    # Limita o tamanho do texto para evitar estouro de memória
    MAX_TOKENS = 256
    email_limpo = clean_text(email)
    email_limpo = email_limpo[:1500]  # Limita caracteres (aprox. 256 tokens)

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
        classifier = get_classifier()
        resposta = classifier(
            email_limpo,
            candidate_labels=candidate_labels,
            hypothesis_template=hypothesis_template,
        )

        if not resposta or "labels" not in resposta or "scores" not in resposta:
            return "ERRO_CLASSIFICACAO"

        melhor_label = resposta["labels"][0]
        if melhor_label == "E-mail relacionado a trabalho/profissional":
            return "PRODUTIVO"
        elif melhor_label == "E-mail pessoal ou não relacionado a trabalho":
            return "IMPRODUTIVO"
        else:
            return "ERRO_CLASSIFICACAO"

    except Exception as e:
        # Não imprime para não poluir logs e economizar recursos
        return "ERRO_CLASSIFICACAO"

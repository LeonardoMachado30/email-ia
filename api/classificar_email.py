from transformers import pipeline
from api.clean_text import clean_text
import torch

# 328M
# O modelo utilizado é o "cross-encoder/nli-distilroberta-base", um modelo de linguagem treinado para tarefas de inferência de linguagem natural (NLI - Natural Language Inference).
# Este modelo é baseado na arquitetura DistilRoBERTa, uma versão compacta e eficiente do RoBERTa, treinada para entender relações semânticas entre pares de sentenças.
# O modelo é capaz de realizar classificação zero-shot, ou seja, pode classificar textos em categorias mesmo sem ter sido treinado especificamente para elas, apenas com base em descrições das categorias (labels).
# Fonte: https://huggingface.co/cross-encoder/nli-distilroberta-base

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=-1,  # Força uso de CPU
    return_all_scores=False,  # Apenas o melhor resultado
    use_fast=True,  # Tokenizer rápido
    model_kwargs={
        "dtype": torch.float16,  # Reduz uso de memória
        "low_cpu_mem_usage": True,
    },
)


def classificar_email(email: str) -> str:
    email_limpo = clean_text(email)

    candidate_labels = [
        "Email profissional relacionado a trabalho",
        "Email pessoal sem relação com trabalho",
    ]

    label_mapeamento = {
        "Email profissional relacionado a trabalho": "PRODUTIVO",
        "Email pessoal sem relação com trabalho": "IMPRODUTIVO",
    }

    try:
        resposta = classifier(
            email_limpo,
            candidate_labels=candidate_labels,
            hypothesis_template="Este email é {}.",
        )

        if not resposta or "labels" not in resposta or "scores" not in resposta:
            return "ERRO_CLASSIFICACAO"

        melhor_label = resposta["labels"][0]
        return label_mapeamento.get(melhor_label, "ERRO_CLASSIFICACAO")

    except Exception as e:
        print(f"Erro na classificação: {e}")
        return "ERRO_CLASSIFICACAO"

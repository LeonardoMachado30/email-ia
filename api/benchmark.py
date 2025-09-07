import psutil
import os
import time
import torch
from transformers import pipeline


def monitor_usage(note=""):
    """Captura uso de RAM e CPU do processo atual"""
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    rss = mem_info.rss / (1024 * 1024)  # MB
    cpu = process.cpu_percent(interval=0.1)
    print(f"[{note}] RAM: {rss:.2f} MB | CPU: {cpu:.2f}%")


def benchmark_model(model_name, sample_text, candidate_labels):
    print(f"\n🚀 Testando modelo: {model_name}\n")

    # Antes de carregar
    monitor_usage("Antes de carregar modelo")

    start_time = time.time()
    classifier = pipeline(
        "zero-shot-classification",
        model=model_name,
        device=-1,  # CPU only
        use_fast=True,
        model_kwargs={
            "dtype": torch.float32,  # Mantém compatibilidade
            "low_cpu_mem_usage": True,
        },
    )
    load_time = time.time() - start_time
    monitor_usage("Após carregar modelo")
    print(f"⏱ Tempo de carregamento: {load_time:.2f}s\n")

    # Rodando inferência
    start_time = time.time()
    result = classifier(sample_text, candidate_labels)
    infer_time = time.time() - start_time
    monitor_usage("Após inferência")
    print(f"⏱ Tempo de inferência: {infer_time:.2f}s")
    print(f"📊 Resultado: {result}\n")


if __name__ == "__main__":
    sample_text = """
    Prezado Flávio,
    Gostaria de confirmar nossa reunião de alinhamento do Projeto X,
    agendada para amanhã às 10h no Google Meet.
    """
    candidate_labels = ["PRODUTIVO", "IMPRODUTIVO"]

    modelos = [
        "valhalla/distilbart-mnli-12-1",
        "facebook/bart-large-mnli",
        "MoritzLaurer/deberta-v3-base-zeroshot-v1",
    ]

    for m in modelos:
        benchmark_model(m, sample_text, candidate_labels)

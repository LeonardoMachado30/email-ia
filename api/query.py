import os
import requests
from typing import Any, Dict, Optional

HF_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

if not HF_TOKEN:
    raise ValueError("Token HF não encontrado no .env")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
}


def query(url: str, payload: Dict[str, Any], timeout: int = 60) -> Optional[dict]:
    """
    Realiza uma requisição POST para a API Hugging Face com autenticação.

    Objetivo:
    - Enviar um payload JSON para um endpoint Hugging Face e retornar a resposta em formato dict.

    Instruções:
    - Informe a URL do endpoint (url) e o payload (dict) conforme a documentação da API.
    - O timeout padrão é 60 segundos.
    - Retorna o JSON da resposta em caso de sucesso, ou None em caso de erro.

    Pontos principais:
    - Autenticação via token Hugging Face.
    - Tratamento de erros HTTP, timeout e exceções de requisição.
    - Retorno padronizado para integração com outros módulos.
    """
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=timeout)

        if response.status_code != 200:
            print(f"Erro HTTP: {response.status_code} - {response.text}")
            return None

        return response.json()

    except requests.Timeout:
        print("Erro: tempo de espera excedido na API.")
        return None
    except requests.RequestException as e:
        print(f"Erro de requisição: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

import os
import requests

HF_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

if not HF_TOKEN:
    raise ValueError("Token HF não encontrado no .env")


API_URL_SUGGESTION = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
}


def query(url, payload, timeout=60):
    try:
        response = requests.post(url, headers=headers, json=payload)

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

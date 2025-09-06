# Gerador de E-mail com IA

Sistema web para análise e geração de e-mails, classificando como **PRODUTIVO** (requere ação/profissional) ou **IMPRODUTIVO** (contexto pessoal) e sugerindo respostas automáticas.

## Funcionalidades

- Classificação de e-mails usando `facebook/bart-large-mnli`.
- Limpeza de texto (remoção de caracteres especiais, links e emojis).
- Upload de arquivos `.txt` e `.pdf`.
- Histórico de e-mails processados via `localStorage`.
- Botões para limpar campos individuais ou todo o formulário.

## Tecnologias

- Python, Flask
- Hugging Face Transformers
- HTML, CSS, JavaScript
- PyPDF2

## Instalação

```bash
git clone https://github.com/LeonardoMachado30/email-ia
cd gerador-email-ia
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

Crie um arquivo `.env` com:

```
HUGGING_FACE_TOKEN=seu_token_aqui
```

Execute o servidor:

```bash
python app.py
```

Acesse `http://127.0.0.1:5000`

## Uso

1. Preencha os campos ou faça upload de arquivo.
2. Clique em **Gerar E-mail**.
3. Visualize resultado e histórico.

## Licença

MIT License

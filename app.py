from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import os

load_dotenv()

from api.process_file import process_file
from api.classificar_email import classificar_email
from api.gerar_resposta_sugerida import gerar_resposta_sugerida

app = Flask(__name__)
app.debug = os.getenv("FLASK_ENV") == "development"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/processar", methods=["POST"])
def processar_email():
    email_content = request.form.get("email_content", "")
    titulo = request.form.get("titulo", "")
    remetente = request.form.get("remetente", "")

    uploaded_file = request.files.get("email_file")
    if uploaded_file:
        try:
            email_content = process_file(uploaded_file)
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    categoria = classificar_email(f"titulo:{titulo}.Corpo:{email_content}")
    resposta_sugerida = gerar_resposta_sugerida(email_content, categoria)

    return jsonify(
        {
            "categoria": categoria,
            "resposta_sugerida": resposta_sugerida,
            "email_content": email_content,
            "remetente": remetente,
            "titulo": titulo,
        }
    )


port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    if app.debug:
        from livereload import Server

        server = Server(app.wsgi_app)
        server.watch("*.py")
        server.watch("templates/*.html")
        server.watch("static/*")
        server.serve(port=5000)
    else:
        # Em produção só roda o Flask
        app.run(host="0.0.0.0", port=port)

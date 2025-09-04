from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from livereload import Server
from tkinter import N

load_dotenv()

from api.process_file import process_file

app = Flask(__name__)
app.debug = True


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

    return jsonify(
        {
            "email_content": email_content,
            "remetente": remetente,
            "titulo": titulo,
        }
    )


if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.watch("*.py")
    server.watch("templates/*.html")
    server.watch("static/*")
    server.serve(port=5000)

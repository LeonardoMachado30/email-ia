from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from livereload import Server
from tkinter import N

load_dotenv()


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

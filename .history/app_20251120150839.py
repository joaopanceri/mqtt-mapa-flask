import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "svg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB, se quiser limitar

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_current_background():
    """
    Procura a última imagem enviada na pasta uploads.
    Para algo mais robusto depois podemos salvar em BD.
    """
    files = [
        f for f in os.listdir(UPLOAD_FOLDER)
        if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))
    ]
    if not files:
        return None

    files = sorted(
        files,
        key=lambda f: os.path.getmtime(os.path.join(UPLOAD_FOLDER, f)),
        reverse=True,
    )
    return files[0]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "background" not in request.files:
            return redirect(url_for("index"))

        file = request.files["background"]

        if file.filename == "":
            return redirect(url_for("index"))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Se quiser padronizar o nome:
            # ext = filename.rsplit(".", 1)[1].lower()
            # filename = f"background.{ext}"
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)
            return redirect(url_for("index"))

    current_bg = get_current_background()
    background_url = None
    if current_bg:
        background_url = url_for("static", filename=f"uploads/{current_bg}")

    # No futuro também vamos mandar para o template a lista de antenas, etc.
    return render_template("index.html", background_url=background_url)


if __name__ == "__main__":
    app.run(debug=True)

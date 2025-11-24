import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_folder="static", static_url_path="/static")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "svg"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# Se quiser limitar tamanho depois, pode voltar com MAX_CONTENT_LENGTH


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_current_background():
    """Retorna o arquivo mais recente na pasta uploads, se existir."""
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
        file = request.files.get("background")

        # Nenhum arquivo selecionado
        if file is None or file.filename == "":
            return redirect(url_for("index"))

        if allowed_file(file.filename):
            # Sempre sobrescreve com um nome padrão (facilita debugging)
            ext = file.filename.rsplit(".", 1)[1].lower()
            filename = secure_filename(f"background.{ext}")
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)

        return redirect(url_for("index"))

    current_bg = get_current_background()
    background_url = (
        url_for("static", filename=f"uploads/{current_bg}") if current_bg else None
    )

    return render_template("index.html", background_url=background_url)


if __name__ == "__main__":
    app.run(debug=True)

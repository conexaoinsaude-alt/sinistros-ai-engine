from flask import Flask, render_template, request, redirect, send_file, url_for
import sqlite3

from reportlab.pdfgen import canvas

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user
)

app = Flask(__name__)

app.secret_key = "supersecretkey"

# LOGIN

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

# USUÁRIO

class User(UserMixin):

    def __init__(self, id):
        self.id = id

USUARIO = {

    "admin": {
        "senha": "1234"
    }

}

@login_manager.user_loader
def load_user(user_id):

    return User(user_id)

# SQLITE

conn = sqlite3.connect(
    "sinistros.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS sinistros (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT,
    status TEXT,
    risco TEXT,
    score INTEGER

)

""")

conn.commit()

# IA

def analisar_risco(descricao):

    descricao = descricao.lower()

    if "queda" in descricao:
        return "MÉDIO", 65

    elif "máquina" in descricao or "elétrica" in descricao:
        return "ALTO", 90

    elif "leve" in descricao:
        return "BAIXO", 30

    else:
        return "MÉDIO", 50

# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        senha = request.form["senha"]

        if username in USUARIO:

            if senha == USUARIO[username]["senha"]:

                user = User(username)

                login_user(user)

                return redirect(url_for("home"))

    return render_template("login.html")

# LOGOUT

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))

# HOME

@app.route("/")
@login_required
def home():

    filtro = request.args.get("risco")

    busca = request.args.get("busca")

    query = "SELECT * FROM sinistros WHERE 1=1"

    params = []

    if filtro and filtro != "TODOS":

        query += " AND risco = ?"

        params.append(filtro)

    if busca:

        query += " AND descricao LIKE ?"

        params.append(f"%{busca}%")

    cursor.execute(query, params)

    sinistros = cursor.fetchall()

    total_sinistros = len(sinistros)

    alto_risco = len([
        s for s in sinistros
        if s[3] == "ALTO"
    ])

    medio_risco = len([
        s for s in sinistros
        if s[3] == "MÉDIO"
    ])

    baixo_risco = len([
        s for s in sinistros
        if s[3] == "BAIXO"
    ])

    media_score = 0

    if total_sinistros > 0:

        media_score = sum([
            s[4] for s in sinistros
        ]) / total_sinistros

    return render_template(

        "index.html",

        sinistros=sinistros,

        total_sinistros=total_sinistros,

        alto_risco=alto_risco,

        medio_risco=medio_risco,

        baixo_risco=baixo_risco,

        media_score=round(media_score, 1)

    )

# ADICIONAR

@app.route("/adicionar", methods=["POST"])
@login_required
def adicionar():

    descricao = request.form["descricao"]

    status = "Em análise"

    risco, score = analisar_risco(descricao)

    cursor.execute("""

    INSERT INTO sinistros
    (descricao, status, risco, score)

    VALUES (?, ?, ?, ?)

    """, (descricao, status, risco, score))

    conn.commit()

    return redirect("/")

# PDF

@app.route("/pdf")
@login_required
def gerar_pdf():

    cursor.execute("SELECT * FROM sinistros")

    sinistros = cursor.fetchall()

    nome_pdf = "relatorio_sinistros.pdf"

    pdf = canvas.Canvas(nome_pdf)

    pdf.setFont("Helvetica-Bold", 18)

    pdf.drawString(
        140,
        800,
        "Relatório Executivo de Sinistros"
    )

    y = 760

    pdf.setFont("Helvetica", 12)

    for s in sinistros:

        pdf.drawString(50, y, f"ID: {s[0]}")
        y -= 20

        pdf.drawString(50, y, f"Descrição: {s[1]}")
        y -= 20

        pdf.drawString(50, y, f"Status: {s[2]}")
        y -= 20

        pdf.drawString(50, y, f"Risco: {s[3]}")
        y -= 20

        pdf.drawString(50, y, f"Score IA: {s[4]}/100")
        y -= 40

    pdf.save()

    return send_file(
        nome_pdf,
        as_attachment=True
    )

if __name__ == "__main__":

    app.run(debug=True)
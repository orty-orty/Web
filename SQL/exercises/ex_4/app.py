from flask import Flask, g, request, redirect, session, render_template_string
import sqlite3
import os
import re
import unicodedata
import html

app = Flask(__name__)
app.secret_key = "supersecretkey"
DATABASE = "database.db"

base_template = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>{{ title }}</title>
<style>
    body {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: monospace;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        text-align: center;
    }
    h2 {
        color: #58a6ff;
    }
    a {
        color: #58a6ff;
        text-decoration: none;
        margin: 5px;
        display: inline-block;
    }
    a:hover {
        text-decoration: underline;
    }
    input, button {
        padding: 5px;
        margin: 5px;
        font-family: monospace;
    }
</style>
</head>
<body>
    {{ content|safe }}
</body>
</html>
"""

def render_custom(content_html, title="Challenge SQLite"):
    """Injecte ton layout custom."""
    return render_template_string(base_template, title=title, content=content_html)

def init_db():
    if os.path.exists(DATABASE):
        try:
            os.remove(DATABASE)
        except PermissionError:
            print("Impossible de supprimer la DB")
            return

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE users (
            username TEXT,
            school TEXT,
            password TEXT
        )
    """)
    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", ("admin", "21", "T0_seCuR3_7o_Be_PWn"))
    conn.commit()
    conn.close()

interdits = ["union", "select", "where", "--", ";", "insert", "delete", "drop"]


@app.route("/")
def home():
    if "username" in session:
        return redirect("/update")
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        school = request.form["school"]
        password_raw = request.form["password"]

        password = html.unescape(unicodedata.normalize("NFKC", password_raw)).lower()

        if not re.fullmatch(r"[a-z=,'\s]+", password):
            return render_custom("<h2>Mot de passe interdit</h2>")

        if any(kw in password for kw in interdits):
            return render_custom("<h2>Mot de passe interdit</h2>")

        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=?", (username,))
            if c.fetchone():
                return render_custom("<h2>Nom déjà pris</h2>")

            c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, school, password))
            conn.commit()

        return redirect("/login")

    html_form = """
    <h2>Créer un compte</h2>
    <form method="POST">
        Nom : <input name="username"><br>
        school : <input name="school"><br>
        Mot de passe : <input name="password"><br>
        <button type="submit">Créer</button>
    </form>
    <a href="/login">Déjà inscrit ?</a>
    """
    return render_custom(html_form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = html.unescape(unicodedata.normalize("NFKC", request.form["password"])).lower()

        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            if c.fetchone():
                session["username"] = username
                return redirect("/update")

        return render_custom("<h2>Échec de connexion</h2>")

    html_form = """
    <h2>Connexion</h2>
    <form method="POST">
        Username : <input name="username"><br>
        Mot de passe : <input name="password"><br>
        <button type="submit">Se connecter</button>
    </form>
    <a href="/register">Créer un compte</a>
    """
    return render_custom(html_form)

@app.route("/update", methods=["GET", "POST"])
def change():
    if "username" not in session:
        return redirect("/login")

    if request.method == "POST":
        school_raw = request.form["school"]
        password_raw = request.form["password"]

        school = html.unescape(unicodedata.normalize("NFKC", school_raw)).lower()
        password = html.unescape(unicodedata.normalize("NFKC", password_raw)).lower()

        
        if any(kw in school for kw in interdits) or not re.fullmatch(r"[a-z=,'\s]+", school):
            return render_custom("<h2>school invalide</h2>")

        if any(kw in password for kw in interdits) or not re.fullmatch(r"[a-z=,'\s]+", password):
            return render_custom("<h2>Mot de passe invalide</h2>")

        username = session["username"]
        query = f"UPDATE users SET school='{school}' WHERE username='{username}' AND password='{password}'"

        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            try:
                c.execute(query)
                conn.commit()
            except Exception as e:
                return render_custom(f"<h2>Erreur SQL : {e}</h2>")

        return render_custom("<h2>school modifié</h2>")

    html_form = """
    <h2>Modification school</h2>
    <form method="POST">
        Nouvel school : <input name="school"><br>
        Mot de passe : <input name="password"><br>
        <button type="submit">Modifier</button>
    </form>
    <a href="/logout">Se déconnecter</a>
    """
    return render_custom(html_form)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if session.get("username") != "admin":
        return render_custom("<h2>Accès interdit</h2>", title="Pannel admin")

    content = f"""
    <h2>Pannel admin</h2>
    <p>Flag : HackUTT{{5Ql1_s3conD_0rdER}}</p>
    <a href="/update">Retour</a>
    """

    return render_custom(content, title="Pannel admin")

@app.route("/reset")
def reset():
    init_db()
    session.clear()
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5004, debug=False)

import random
import sqlite3
from flask import Flask, request, render_template_string, redirect, url_for, session, abort

app = Flask(__name__)
app.secret_key = "supersecuresecretkey"
db = "ex_1.db"

def init_db():
    conn = sqlite3.connect(db)
    curs = conn.cursor()
    curs.execute("DROP TABLE IF EXISTS users")
    curs.execute("""CREATE TABLE users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE,
                 password TEXT
                 )
                 """)
    users = [
        ("alice", "superpass"),
        ("bob", "password123"),
        ("toto", "tropsecure"),
        ("admin", str(random.randint(10000000,99999999))),
        ("tata", "hackutt4ever")
    ]
    curs.executemany("INSERT INTO users (username, password) VALUES (?, ?)", users)
    conn.commit()
    conn.close()

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
        font-family: "Courier New", monospace;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        text-align: center;
    }
    h2 {
        color: #58a6ff;
        text-shadow: 0 0 5px #58a6ff, 0 0 10px #58a6ff;
    }
    input {
        padding: 10px;
        margin: 5px;
        border-radius: 5px;
        border: 1px solid #30363d;
        background-color: #161b22;
        color: #c9d1d9;
    }
    button {
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        background-color: #238636;
        color: #ffffff;
        cursor: pointer;
        font-weight: bold;
        transition: 0.2s;
        box-shadow: 0 0 5px #238636;
        margin-top: 10px;
    }
    button:hover {
        background-color: #2ea043;
        box-shadow: 0 0 10px #2ea043;
    }
    form {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 20px;
    }
</style>
</head>
<body>
    <div>
        {{ content|safe }}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    user = session.get("username")
    if user:
        logout_button = '<form action="/logout" method="post"><button type="submit">Déconnexion</button></form>'
        content = f"<h2>Bienvenu {user} !</h2>{logout_button}"
        return render_template_string(base_template, title="Accueil", content=content)
    login_form = '''
    <h2>Login</h2>
    <form action="/login" method="post">
        username: <input name="username"><br>
        password: <input name="password"><br>
        <button type="submit">Login</button>
    </form>
    '''
    return render_template_string(base_template, title="Login", content=login_form)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    sql_login = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    conn = sqlite3.connect(db)
    curs = conn.cursor()
    try:
        curs.execute(sql_login)
        user = curs.fetchone()
    except Exception as e:
        conn.close()
        return f"Erreur SQL : {e}", 500

    conn.close()

    if user:
        session["username"] = user[1]
        if user[1] == "admin":
            return redirect(url_for("flag"))
        return redirect(url_for("index"))
    else:
        return render_template_string(base_template, title="Login", content="<h2>username ou password incorrect</h2>")

@app.route("/flag", methods=["GET"])
def flag():
    if session.get("username") == "admin":
        content = "<h2>GG le flag est : HackUTT{M4_pr3m1ERe_Inj3cTI0n}</h2>"
        return render_template_string(base_template, title="Flag", content=content)
    else:
        abort(403)

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=False, host="0.0.0.0", port=5001)




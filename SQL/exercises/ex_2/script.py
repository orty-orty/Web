import sqlite3
from flask import Flask, request, render_template_string, redirect, url_for, session, abort

app = Flask(__name__)
app.secret_key = "supersecuresecretkey"
db = "ex_2.db"

def init_db():
    conn = sqlite3.connect(db)
    curs = conn.cursor()
    curs.execute("DROP TABLE IF EXISTS users")
    curs.execute("DROP TABLE IF EXISTS items")
    curs.execute("""CREATE TABLE users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE,
                 password TEXT
                 )
                 """)

    curs.execute("""CREATE TABLE items (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT UNIQUE,
                     price TEXT
                     )
                     """)
    users = [
        ("alice", "superpass"),
        ("bob", "password123"),
        ("toto", "tropsecure"),
        ("admin", "HackUTT{Un10n_b4sE_iNj3c7Ion}"),
        ("tata", "hackutt4ever")
    ]

    items = [
        ("hat", "20$"),
        ("sweat", "60$"),
        ("basket", "110$"),
        ("glasses", "15$"),
        ("stickers", "1$")
    ]

    curs.executemany("INSERT INTO users (username, password) VALUES (?, ?)", users)
    conn.commit()
    curs.executemany("INSERT INTO items (name, price) VALUES (?,?)", items)
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
</style>
</head>
<body>
    {{ content|safe }}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    conn = sqlite3.connect(db)
    curs = conn.cursor()
    curs.execute("SELECT name FROM items")
    items = curs.fetchall()
    conn.close()

    content = "<h2>Bienvenue, voici une sélection des articles proposés très prochainement chez HackUTT !</h2><ul>"
    for item in items:
        content += f'<li><a href="/item?name={item[0]}">{item[0]}</a></li>'
    content += "</ul>"

    return render_template_string(base_template, title="Item List", content=content)


@app.route("/item", methods=["GET"])
def item():
    name = request.args.get("name", "")

    conn = sqlite3.connect(db)
    curs = conn.cursor()

    # ⚠️ Vulnérabilité SQLi ici : injection possible via "name"
    query = f"SELECT * FROM items WHERE name = '{name}'"
    try:
        curs.execute(query)
        result = curs.fetchone()
    except Exception as e:
        result = None

    conn.close()

    if result:
        content = f"<h2>Item info</h2><p>Name: {result[1]}<br>Price: {result[2]}</p>"
    else:
        content = "<p>Item not found</p>"

    return render_template_string(base_template, title="Item Info", content=content)


if __name__ == "__main__":
    init_db()
    app.run(debug=False, host="0.0.0.0", port=5001)

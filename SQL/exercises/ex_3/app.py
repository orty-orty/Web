import os
import html
from flask import Flask, request, render_template_string
import psycopg2
from psycopg2 import DatabaseError

app = Flask(__name__)
app.secret_key = "change_this_for_lab_only"

DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = int(os.environ.get("DB_PORT", 5432))
DB_NAME = os.environ.get("DB_NAME", "labdb")
DB_USER = os.environ.get("DB_USER", "labuser")
DB_PASS = os.environ.get("DB_PASS", "labpass")

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

def get_conn():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASS
    )

@app.route("/", methods=["GET"])
def index():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT name FROM items ORDER BY id")
    items = cur.fetchall()
    cur.close()
    conn.close()

    content = "<h2>Bienvenue — items</h2><ul>"
    for it in items:
        content += f'<li><a href="/item?name={html.escape(it[0])}">{html.escape(it[0])}</a></li>'
    content += "</ul>"

    return render_template_string(base_template, title="Items", content=content)

@app.route("/item", methods=["GET"])
def item():
    name = request.args.get("name", "")

    query = f"SELECT * FROM items WHERE name = '{name}'"

    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute(query)
        row = cur.fetchone()

    except DatabaseError as e:
        conn.close()
        content = f"<h2>SQL Error</h2><pre>{html.escape(str(e))}</pre>"
        return render_template_string(base_template, title="Erreur SQL", content=content)

    conn.close()

    if row:
        content = f"""
        <h2>Item info</h2>
        <p>Name: {html.escape(str(row[1]))}<br>
        Price: {html.escape(str(row[2]))}</p>
        """
    else:
        content = "<p>Item not found</p>"

    return render_template_string(base_template, title="Item Info", content=content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)

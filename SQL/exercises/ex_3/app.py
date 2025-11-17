import os
import html
from flask import Flask, request, render_template_string
import psycopg2
from psycopg2 import sql, OperationalError, DatabaseError

app = Flask(__name__)
app.secret_key = "change_this_for_lab_only"

DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = int(os.environ.get("DB_PORT", 5432))
DB_NAME = os.environ.get("DB_NAME", "labdb")
DB_USER = os.environ.get("DB_USER", "labuser")
DB_PASS = os.environ.get("DB_PASS", "labpass")

base_template = """
<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><title>{{ title }}</title>
<style>
 body{background:#0d1117;color:#c9d1d9;font-family:monospace;padding:20px}
 code{background:#0b1220;padding:2px 6px;border-radius:4px}
 a{color:#58a6ff}
</style></head><body>
  {{ content|safe }}
</body></html>
"""

def get_conn():
    return psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)

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

    # vulnérable volontairement : concaténation directe
    query = f"SELECT * FROM items WHERE name = '{name}'"

    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(query)
        row = cur.fetchone()
    except DatabaseError as e:
        # POSTGRES will raise e.g. division_by_zero or invalid input syntax for integer
        # For pedagogical demo: fetch admin password (dangerous) and show message
        try:
            cur.execute("SELECT password FROM users WHERE username='admin' LIMIT 1")
            pwrow = cur.fetchone()
            password = pwrow[0] if pwrow else "<no-password>"
        except Exception:
            password = "<error-reading-password>"

        conn.close()
        safe_pw = html.escape(str(password))
        safe_query = html.escape(query)
        content = (
            "<h2>Erreur pédagogique</h2>"
            f"<p><strong>Requête :</strong><br><code>{safe_query}</code></p>"
            f"<p><strong>Message DB :</strong><br><code>{html.escape(str(e))}</code></p>"
            f"<p><strong>Leak (demo):</strong> you can't divide <code>{safe_pw}</code> by zero</p>"
        )
        return render_template_string(base_template, title="Erreur (DB)", content=content)

    # Si pas d'exception, vérifier row
    if row is not None and any(col is None for col in row):
        # si une colonne est NULL, on peut aussi considérer ça comme une "erreur logic" (rare en PG)
        try:
            cur.execute("SELECT password FROM users WHERE username='admin' LIMIT 1")
            pwrow = cur.fetchone()
            password = pwrow[0] if pwrow else "<no-password>"
        except Exception:
            password = "<error-reading-password>"
        conn.close()
        safe_pw = html.escape(str(password))
        safe_query = html.escape(query)
        content = (
            "<h2>Erreur pédagogique (NULL détecté)</h2>"
            f"<p><strong>Requête :</strong><br><code>{safe_query}</code></p>"
            f"<p><strong>Leak (demo):</strong> you can't divide <code>{safe_pw}</code> by zero</p>"
        )
        return render_template_string(base_template, title="Erreur (NULL)", content=content)

    conn.close()

    if row:
        content = f"<h2>Item info</h2><p>Name: {html.escape(str(row[1]))}<br>Price: {html.escape(str(row[2]))}</p>"
    else:
        content = "<p>Item not found</p>"

    return render_template_string(base_template, title="Item Info", content=content)

if __name__ == "__main__":
    # Permet d'exécuter aussi localement sans Docker si tu veux
    app.run(host="0.0.0.0", port=5001)

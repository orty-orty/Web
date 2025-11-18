import os
from flask import Flask, request, render_template_string
import mysql.connector
from mysql.connector import Error
import time
import html

app = Flask(__name__)

def init_db():
    for i in range(10):
        try:
            cursor = db.cursor()

            cursor.execute("DROP TABLE IF EXISTS products")

            cursor.execute("""
                CREATE TABLE products (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255),
                    price VARCHAR(255),
                    description TEXT
                )
            """)

            cursor.execute("""
                INSERT INTO products (name, price, description)
                VALUES ('T-Shirt HackUTT', '25$', 'Disponible bientôt !')
            """)

            db.commit()
            cursor.close()
            print("✔ Base MySQL initialisée.")
            return

        except Exception as e:
            print("MySQL pas prêt, tentative suivante...", e)
            time.sleep(2)

    print("❌ Impossible d'initialiser MySQL")



db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)


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

@app.route("/")
def home():
    content = "<h2>Try /product?id=1</h2>"
    return render_template_string(base_template, content=content, title="Home")


@app.route("/product")
def product():
    pid = request.args.get("id", "")

    cursor = db.cursor()

    query = f"SELECT name, price, description FROM products WHERE id = '{pid}'"

    try:
        cursor.execute(query)
        row = cursor.fetchone()

    except Error as e:

        return render_template_string(
            base_template,
            content=f"<h2>SQL ERROR</h2><pre>{html.escape(str(e))}</pre>",
            title="SQL Error"
        )


    if row:
        safe_row = []
        for col in row:
            try:
                safe_row.append(html.escape(str(col)))
            except:
                safe_row.append("<?>")


        while len(safe_row) < 3:
            safe_row.append("")

        name, price, description = safe_row[:3]

    else:
        name = price = description = "None"


    cursor.close()

    content = f"""
    <h2>Item info</h2>
    <p><b>Name:</b> {name}</p>
    <p><b>Price:</b> {price}</p>
    <p><b>Description:</b></p>
    <pre>{description}</pre>
    """

    return render_template_string(base_template, content=content, title="Product")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5005)

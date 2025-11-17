import os
from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)

@app.route("/")
def home():
    return render_template("base.html", content="<h2>Try /product?id=1</h2>", title="Home")

@app.route("/product")
def product():
    pid = request.args.get("id", "")

    cursor = db.cursor()

    query = f"SELECT name, price, description FROM products WHERE id = '{pid}'"

    try:
        cursor.execute(query)
        row = cursor.fetchone()

        if row:
            name, price, description = row
        else:
            name = price = description = "None"

        content = f"""
        <h2>Item info</h2>
        <p><b>Name:</b> {name}</p>
        <p><b>Price:</b> {price}</p>
        <p><b>Description:</b></p>
        <pre>{description}</pre>
        """
        return render_template("base.html", content=content, title="Product")

    except Exception as e:
        return render_template("base.html", content=f"<pre>SQL ERROR: {e}</pre>", title="SQL Error")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)

from flask import Flask, request, render_template_string
import mysql.connector
import os

app = Flask(__name__)

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
    .result {
        margin-top: 20px;
        padding: 10px;
        background-color: #161b22;
        border-radius: 5px;
        max-width: 800px;
    }
    table {
        margin: 0 auto;
        border-collapse: collapse;
    }
    td {
        padding: 10px;
        border: 1px solid #30363d;
    }
</style>
</head>
<body>
    {{ content|safe }}
</body>
</html>
"""

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="ctf_user",
        password="ctf_password",
        database="ctf_db"
    )

@app.route('/')
def index():
    content = """
    <h2>🔍 Recherche d'articles</h2>
    <p>Recherchez un article par son ID</p>
    <form action="/search" method="GET">
        <input type="text" name="id" placeholder="ID de l'article" required>
        <button type="submit">Rechercher</button>
    </form>
    """
    return render_template_string(base_template, title="SQLi Challenge", content=content)

@app.route('/search')
def search():
    article_id = request.args.get('id', '')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Requête vulnérable (injection SQL évidente)
        query = f"SELECT title, author, content FROM articles WHERE id = {article_id}"
        cursor.execute(query)
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if results:
            result_html = '<div class="result"><h3>Résultats :</h3><table>'
            for row in results:
                result_html += f"<tr><td><strong>Titre:</strong> {row[0]}</td></tr>"
                result_html += f"<tr><td><strong>Auteur:</strong> {row[1]}</td></tr>"
                result_html += f"<tr><td><strong>Contenu:</strong> {row[2]}</td></tr>"
                result_html += "<tr><td>---</td></tr>"
            result_html += '</table></div>'
        else:
            result_html = '<div class="result"><p>Aucun article trouvé.</p></div>'
        
        content = f"""
        <h2>🔍 Recherche d'articles</h2>
        <form action="/search" method="GET">
            <input type="text" name="id" placeholder="ID de l'article" value="{article_id}" required>
            <button type="submit">Rechercher</button>
        </form>
        {result_html}
        <br>
        <a href="/">← Retour</a>
        """
        
        return render_template_string(base_template, title="Résultats", content=content)
    
    except Exception as e:
        content = f"""
        <h2>❌ Erreur</h2>
        <p>Une erreur est survenue lors de la recherche.</p>
        <p style="color: #f85149;">{str(e)}</p>
        <a href="/">← Retour</a>
        """
        return render_template_string(base_template, title="Erreur", content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=False)

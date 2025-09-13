import sqlite3
from tabulate import tabulate

#on se connecte à une db en mémoire
connexion = sqlite3.connect("database")
curseur = connexion.cursor()


def reset_db():
    curseur.execute("DROP TABLE IF EXISTS users")
    # création des tables
    curseur.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, age INTEGER, email TEXT, password TEXT)")
    # initialisation de la db (on ajoute juste des users)
    curseur.execute("INSERT INTO users (username , age, email, password) VALUES (?, ?, ?, ?)",
                    ("Toto", 30, "toto@hackutt.fr", "123456"))
    curseur.execute("INSERT INTO users (username , age, email, password) VALUES (?, ?, ?, ?)",
                    ("Alice", 23, "alice@hackutt.fr", "superpass"))
    curseur.execute("INSERT INTO users (username , age, email, password) VALUES (?, ?, ?, ?)",
                    ("Bob", 37, "bob@hackutt.fr", "tropsecure"))
    curseur.execute("INSERT INTO users (username , age, email, password) VALUES (?, ?, ?, ?)",
                    ("admin", 100, "admin@hackutt.fr", "ortylegigabg"))
    curseur.execute("INSERT INTO users (username , age, email, password) VALUES (?, ?, ?, ?)",
                    ("Tata", 56, "tata@hackutt.fr", "flemme"))
    connexion.commit()
    affiche_db()

def affiche_db():
    curseur.execute("SELECT * FROM users")
    ligne = curseur.fetchall()
    headers = [desc[0] for desc in curseur.description]
    print("affichage de la db...\n")
    print(tabulate(ligne, headers=headers, tablefmt="db"))
    print("\n")

def register():
    print("Vous pouvez désormais vous enregistrer")
    username = str(input("entrez votre pseudo : "))
    age = int(input("entrez votre age : "))
    email = str(input("entrez votre email : "))
    password = str(input("entrez votre mot de passe : "))
    #la requete sql arrive
    curseur.execute("INSERT INTO users (username, age, email, password) VALUES (?, ?, ?, ?)", (username, age, email, password))
    connexion.commit()
    print(f"la requête effectuée est : \"INSERT INTO users (username, age, email, password) VALUES (?, ?, ?, ?)\", ({username}, {age}, {email}, {password}))\n")
    affiche_db()

def login():
    print("Entrez vos informations pour vous connecter")
    username_log = str(input("entrez votre pseudo : "))
    pass_log = str(input("entrez votre mot de passe : "))
    curseur.execute("SELECT * FROM users WHERE username=? AND password=?", (username_log,pass_log))
    utilisateur = curseur.fetchone()
    if utilisateur:
        print(f"connexion réussie, bienvenue chez HackUTT {username_log}")
    else:
        print("username ou password incorrect")
    print(f"la requête effectuée est : \"SELECT * FROM users WHERE username=? AND password=?\", ({username_log},{pass_log}))\n")
    affiche_db()
    return utilisateur is not None

def update_mdp():
    username_reset = str(input("entrez le pseudo du user dont vous voulez changer le mot de passe : "))
    pass_reset = str(input("entrez son nouveau mot de passe : "))
    curseur.execute("UPDATE users SET password=? WHERE username=?",(username_reset, pass_reset))
    connexion.commit()
    print(f"la reqête effectuée est : \"UPDATE users SET password=? WHERE username=?\",(username_reset, pass_reset)")
    affiche_db()

def requete_yolo():
    request = input("entrez la requête que vous voulez effectuer : ")
    try:
        curseur.execute(request)
        connexion.commit()
        print("requête exécutée avec succès.")
        affiche_db()
    except Exception as e:
        print("erreur SQL : ", e)



#lancement de l'exo
reset_db()
while True:
    choix = str(input("Que voulez vous faire ?\nEntrez le numéro de votre choix.\n"
                "(1) afficher la db\n"
                "(2) register\n"
                "(3) login\n"
                "(4) changer de mot de passe\n"
                "(5) réinitialiser la db\n"
                "(6) faites votre propre requête ;)\n"))
    match choix:
        case "1":
            affiche_db()
        case "2":
            register()
        case "3":
            login()
        case "4":
            update_mdp()
        case "5":
            reset_db()
        case "6":
            requete_yolo()





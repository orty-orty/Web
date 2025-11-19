#!/bin/bash

# Démarrer MySQL en arrière-plan
mysqld_safe --datadir=/var/lib/mysql &

# Attendre que MySQL soit prêt
echo "Démarrage de MySQL..."
for i in {1..30}; do
    if mysqladmin ping -h localhost --silent; then
        echo "MySQL est prêt !"
        break
    fi
    echo "Attente de MySQL... ($i/30)"
    sleep 2
done

# Vérifier si MySQL a démarré
if ! mysqladmin ping -h localhost --silent; then
    echo "Erreur: MySQL n'a pas démarré"
    exit 1
fi

# Exécuter le script d'initialisation
echo "Initialisation de la base de données..."
mysql < /app/init.sql

# Configurer MySQL pour LOAD_FILE
echo "Configuration de MySQL pour LOAD_FILE..."
mysql -e "SET GLOBAL local_infile = 1;"
mysql -e "SET GLOBAL secure_file_priv = 'NULL';"

# Vérifier les permissions du flag
ls -la /var/lib/mysql/flag.txt

echo "Base de données initialisée !"
echo "Démarrage de l'application Flask..."

# Lancer l'application Flask
python3 app.py

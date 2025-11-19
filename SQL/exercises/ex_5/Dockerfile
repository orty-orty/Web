FROM python:3.11-slim

# Installation de MySQL et dépendances
RUN apt-get update && apt-get install -y \
    mariadb-server \
    mariadb-client \
    && rm -rf /var/lib/apt/lists/*

# Création du répertoire de travail
WORKDIR /app

# Copie des fichiers
COPY requirements.txt .
COPY app.py .
COPY init.sql .
COPY start.sh .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Initialisation de MySQL et permissions
RUN mysql_install_db --user=mysql --datadir=/var/lib/mysql && \
    chmod +x start.sh && \
    mkdir -p /var/run/mysqld && \
    chown -R mysql:mysql /var/run/mysqld /var/lib/mysql

# Création du flag dans un endroit accessible par MySQL
RUN echo "HackUTT{R3ad_f1le_fr0m_1ns1de_c0nt41ner}" > /flag.txt && \
    chown mysql:mysql /flag.txt && \
    chmod 644 /flag.txt

# Exposition du port
EXPOSE 5005

# Démarrage
CMD ["./start.sh"]

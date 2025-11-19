CREATE DATABASE IF NOT EXISTS ctf_db;
USE ctf_db;

CREATE USER IF NOT EXISTS 'ctf_user'@'localhost' IDENTIFIED BY 'ctf_password';
GRANT ALL PRIVILEGES ON ctf_db.* TO 'ctf_user'@'localhost';
GRANT FILE ON *.* TO 'ctf_user'@'localhost';
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS articles (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    content TEXT
);

INSERT INTO articles (id, title, author, content) VALUES
(1, 'Introduction à la Cybersécurité', 'Alice Dupont', 'La cybersécurité est un domaine passionnant qui protège nos systèmes informatiques.'),
(2, 'Les bases de SQL', 'Bob Martin', 'SQL est un langage utilisé pour interagir avec les bases de données relationnelles.'),
(3, 'Web Application Security', 'Charlie Bernard', 'Sécuriser une application web nécessite de comprendre les vulnérabilités courantes.');

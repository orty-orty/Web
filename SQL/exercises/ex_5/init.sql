CREATE DATABASE IF NOT EXISTS sqli;
USE sqli;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255),
  password VARCHAR(255)
);

INSERT INTO users (username, password) VALUES ('admin', 'admin');

SET GLOBAL secure_file_priv = '';

GRANT FILE ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;

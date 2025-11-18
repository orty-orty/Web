CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    price VARCHAR(255),
    description TEXT
);

INSERT INTO products (name, price, description) VALUES
('T-Shirt HackUTT', '25$', 'Bientôt dispo !');

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255),
  password VARCHAR(255)
);

INSERT INTO users (username, password) VALUES ('admin', 'admin');

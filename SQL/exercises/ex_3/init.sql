CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE,
  password TEXT
);

CREATE TABLE IF NOT EXISTS items (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE,
  price TEXT
);

INSERT INTO users (username, password) VALUES
  ('alice','superpass'),
  ('bob','password123'),
  ('toto','tropsecure'),
  ('admin','HackUTT{Err0r_b4sE_PG}'),
  ('tata','hackutt4ever')
ON CONFLICT DO NOTHING;

INSERT INTO items (name, price) VALUES
  ('hat','20$'),
  ('sweat','60$'),
  ('basket','110$'),
  ('glasses','15$'),
  ('stickers','1$')
ON CONFLICT DO NOTHING;

-- Tabela users
CREATE TABLE IF NOT EXISTS users (
  id   SERIAL PRIMARY KEY,
  name TEXT    NOT NULL,
  email TEXT   UNIQUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Tabela posts powiązana z users
CREATE TABLE IF NOT EXISTS posts (
  id      SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title   TEXT    NOT NULL,
  body    TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

INSERT INTO users (name, email) VALUES
  ('Alice','alice@example.com'),
  ('Bob','bob@example.com')
ON CONFLICT DO NOTHING;

INSERT INTO posts (user_id, title, body) VALUES
  (1, 'Witaj świecie','To jest mój pierwszy post.'),
  (2, 'Hej!','Bob pisze coś.');

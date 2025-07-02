-- 1. Rozszerzenie tabeli users o profil:
ALTER TABLE users
  ADD COLUMN bio       TEXT,
  ADD COLUMN avatar_url TEXT;

-- 2. Tabela comments:
CREATE TABLE IF NOT EXISTS comments (
  id         SERIAL PRIMARY KEY,
  post_id    INT NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  user_id    INT NOT NULL REFERENCES users(id) ON DELETE SET NULL,
  content    TEXT    NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 3. Kategorie:
CREATE TABLE IF NOT EXISTS categories (
  id    SERIAL PRIMARY KEY,
  name  TEXT UNIQUE NOT NULL
);

-- 4. Przypisanie postów do kategorii:
CREATE TABLE IF NOT EXISTS post_categories (
  post_id     INT NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  category_id INT NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
  PRIMARY KEY (post_id, category_id)
);

-- 5. Tagowanie:
CREATE TABLE IF NOT EXISTS tags (
  id   SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS post_tags (
  post_id INT NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  tag_id  INT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (post_id, tag_id)
);

-- 6. Polubienia:
CREATE TABLE IF NOT EXISTS likes (
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  post_id INT NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT now(),
  PRIMARY KEY (user_id, post_id)
);

INSERT INTO categories (name) VALUES
  ('Tech'),
  ('Lifestyle'),
  ('News')
ON CONFLICT DO NOTHING;

INSERT INTO tags (name) VALUES
  ('python'),
  ('docker'),
  ('sql'),
  ('webdev')
ON CONFLICT DO NOTHING;

-- 8. Przykładowe powiązania
INSERT INTO post_categories (post_id, category_id)
SELECT p.id, c.id
FROM posts p
JOIN categories c ON c.name = 'Tech'
WHERE p.title ILIKE '%Witaj%'
ON CONFLICT DO NOTHING;

INSERT INTO post_tags (post_id, tag_id)
SELECT p.id, t.id
FROM posts p
JOIN tags t ON t.name = 'python'
WHERE p.title ILIKE '%Witaj%'
ON CONFLICT DO NOTHING;

-- 9. Przykładowe komentarze i polubienia
INSERT INTO comments (post_id, user_id, content) VALUES
  (1, 2, 'Świetny wpis, dzięki!'),
  (2, 1, 'Ciekawa perspektywa.');

INSERT INTO likes (user_id, post_id) VALUES
  (1, 2),
  (2, 1);

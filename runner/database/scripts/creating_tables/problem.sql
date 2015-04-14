CREATE TABLE IF NOT EXISTS problems (
  id_problem INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR NOT NULL,
  text VARCHAR NOT NULL,
  language INTEGER,
  FOREIGN KEY (language) REFERENCES languages(id_language),
  UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS solutions (
  id_problem INTEGER,
  code VARCHAR NOT NULL,
  id_lang INTEGER,
  FOREIGN KEY (id_problem) REFERENCES problems(id_problem) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (id_lang) REFERENCES code_languages(id_code_lang) ON UPDATE CASCADE ON DELETE CASCADE,
  UNIQUE (id_problem, code)
);

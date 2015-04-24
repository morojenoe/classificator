CREATE TABLE IF NOT EXISTS solutions (
  id_problem INTEGER,
  code VARCHAR NOT NULL,
  language VARCHAR NOT NULL,
  FOREIGN KEY (id_problem) REFERENCES problems(id_problem) ON UPDATE CASCADE ON DELETE CASCADE,
  UNIQUE (id_problem, code)
);

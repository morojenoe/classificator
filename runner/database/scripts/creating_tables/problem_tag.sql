CREATE TABLE IF NOT EXISTS problem_tag (
  id_problem INTEGER ,
  id_tag INTEGER,
  FOREIGN KEY (id_problem) REFERENCES problems(id_problem) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (id_tag) REFERENCES tags(id_tag)  ON UPDATE CASCADE ON DELETE CASCADE,
  UNIQUE (id_problem, id_tag)
);

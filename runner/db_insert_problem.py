from itertools import izip


def insert_problem_text(cursor, link, text):
    cursor.execute('INSERT INTO problems (link, text, language) VALUES(?,?)', (link, text))


def insert_solutions(cursor, solutions, problem_id):
    code_text = [sol.code for sol in solutions]
    code_lang = [sol.language for sol in solutions]
    rows = izip(problem_id, code_text, code_lang)
    cursor.executemany('INSERT INTO solutions (id_problem, code, id_lang) VALUES(?,?,?)', rows)


def insert_problem_tag(cursor, tags, problem_id):
    rows = zip([problem_id]*len(tags), tags)
    cursor.executemany('INSERT INTO problem_tag (id_problem, id_tag) VALUES(?,?)', rows)


def insert_problem(cursor, problem, tags):
    insert_problem_text(cursor, problem.link, problem.statement)
    problem_id = cursor.lastrowid
    insert_solutions(cursor, problem.submits, problem_id)
    insert_problem_tag(cursor, tags, problem_id)

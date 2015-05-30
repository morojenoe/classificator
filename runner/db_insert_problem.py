def _insert_problem_text(cursor, link, text):
    cursor.execute('INSERT OR IGNORE INTO problems (link, text) VALUES(?,?)', (link, text))


def _insert_solutions(cursor, solutions, problem_id):
    code_text = [sol.code for sol in solutions]
    code_lang = [sol.language for sol in solutions]
    rows = zip([problem_id]*len(solutions), code_text, code_lang)
    cursor.executemany('INSERT OR IGNORE INTO solutions (id_problem, code, language) VALUES(?,?,?)', rows)


def _get_all_tags(cursor):
    cursor.execute('SELECT id_tag, eng_name FROM tags')
    return {tag[1]: tag[0] for tag in cursor}


def _insert_problem_tag(cursor, tags, problem_id):
    all_tags = _get_all_tags(cursor)
    rows = zip([problem_id]*len(tags), [all_tags[tag] for tag in tags])
    cursor.executemany('INSERT OR IGNORE INTO problem_tag (id_problem, id_tag) VALUES(?,?)', rows)


def insert_problem(cursor, problem, tags):
    _insert_problem_text(cursor, problem.link, problem.statement)
    problem_id = cursor.lastrowid
    _insert_solutions(cursor, problem.solutions, problem_id)
    _insert_problem_tag(cursor, tags, problem_id)

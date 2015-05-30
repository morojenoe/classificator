from problem import Problem


def _get_solutions(conn, problem_id):
    cursor = conn.cursor()
    cursor.execute('SELECT code, language FROM solutions WHERE id_problem=?', (problem_id, ))
    return cursor.fetchall()


def _get_tags(conn, problem_id):
    cursor = conn.cursor()
    cursor.execute('SELECT tags.eng_name '
                   'FROM problem_tag '
                   'INNER JOIN tags '
                   'ON tags.id_tag = problem_tag.id_tag '
                   'WHERE problem_tag.id_problem=?', (problem_id, ))
    return [tag[0] for tag in cursor]


def get_problems(conn):
    problems, tags = [], []
    cursor = conn.cursor()
    cursor.execute('SELECT id_problem, link, text '
                   'FROM problems p '
                   'WHERE EXISTS(SELECT * FROM problem_tag pt WHERE pt.id_problem = p.id_problem) ')
    for problem in cursor:
        problem_id = problem[0]
        problems.append(Problem(problem[2], problem[1], _get_solutions(conn, problem_id)))
        tags.append(_get_tags(conn, problem_id))

    return problems, tags

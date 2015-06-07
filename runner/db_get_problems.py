from problem import Problem


def _get_solutions(conn, problem_id):
    cursor = conn.cursor()
    cursor.execute('SELECT code, language FROM solutions WHERE id_problem=?', (problem_id, ))
    return cursor.fetchall()


def _get_tags(conn, problem_id):
    cursor = conn.cursor()
    cursor.execute('SELECT t.eng_name '
                   'FROM problem_tag pt '
                   'INNER JOIN tags t '
                   'ON t.id_tag = pt.id_tag AND t.is_active '
                   'WHERE pt.id_problem=?', (problem_id, ))
    return [tag[0] for tag in cursor]


def get_problems(conn):
    problems, tags = [], []
    cursor = conn.cursor()
    cursor.execute('SELECT id_problem, link, text '
                   'FROM problems p '
                   'WHERE EXISTS(SELECT * '
                   '             FROM problem_tag pt '
                   '             INNER JOIN tags t '
                   '             ON pt.id_tag = t.id_tag AND t.is_active '
                   '             WHERE pt.id_problem = p.id_problem)')
    for problem in cursor:
        problem_id = problem[0]
        problems.append(Problem(problem[2], problem[1], _get_solutions(conn, problem_id)))
        tags.append(_get_tags(conn, problem_id))

    return problems, tags

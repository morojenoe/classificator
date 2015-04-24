from problem import Problem


def get_solutions(conn, problem_id):
    cursor = conn.cursor()
    cursor.execute('SELECT code, language FROM solutions WHERE id_problem=?', (problem_id, ))
    return cursor.fetchall()


def get_tags(conn, problem_id):
    cursor = conn.cursor()
    cursor.execute('SELECT id_tag FROM problem_tag WHERE id_problem=?', (problem_id, ))
    return [tag[0] for tag in cursor]


def get_problems(conn):
    problems, tags = [], []
    cursor = conn.cursor()
    cursor.execute('SELECT id_problem, link, text FROM problems')
    for problem in cursor:
        print problem
        problem_id = problem[0]
        problems.append(Problem(problem[2], problem[1], get_solutions(conn, problem_id)))
        tags.append(get_tags(conn, problem_id))

    return problems, tags

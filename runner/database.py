from path import Path
from sqlite3 import connect as sqlite_connect
from problems_from_codeforces import get_problems as codeforces_problems
from itertools import izip
from db_insert_problem import insert_problem
from db_get_problems import get_problems


PATH_TO_PROBLEM_DATABASE = Path().getcwd().joinpath('database', 'problems.sqlite3')
PATH_TO_SCRIPTS_FOR_CREATING_TABLES = Path().getcwd().joinpath('database', 'scripts', 'creating_tables')
PATH_TO_SCRIPTS_FOR_FILLING_TABLES = Path().getcwd().joinpath('database', 'scripts', 'filling_tables')


def get_script(path_to_script):
    return "".join(Path(path_to_script).lines())


def execute_scripts_from_files(connection, path_to_scripts):
    for script in path_to_scripts:
        connection.executescript(get_script(script))


def create_database(conn):
    execute_scripts_from_files(conn, PATH_TO_SCRIPTS_FOR_CREATING_TABLES.files('*.sql'))
    execute_scripts_from_files(conn, PATH_TO_SCRIPTS_FOR_FILLING_TABLES.files('*.sql'))
    conn.commit()


def fill_database(conn):
    cursor = conn.cursor()
    problems, tags = codeforces_problems()
    for problem, tag in izip(problems, tags):
        insert_problem(cursor, problem, tag)
    conn.commit()


def get_learning_set():
    db_is_exist = Path(PATH_TO_PROBLEM_DATABASE).exists()
    with sqlite_connect(PATH_TO_PROBLEM_DATABASE) as conn:
        if not db_is_exist:
            create_database(conn)
            fill_database(conn)
        return get_problems(conn)

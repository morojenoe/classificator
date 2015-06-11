from path import Path
from sqlite3 import connect as sqlite_connect
from .problems_from_codeforces import CodeforcesDownloader
from .problems_from_timus import TimusDownloader
from .db_insert_problem import insert_problem
from .db_get_problems import get_problems


PATH_TO_PROBLEM_DATABASE = Path().getcwd().joinpath('runner', 'database', 'problems.sqlite3')
PATH_TO_SCRIPTS_FOR_CREATING_TABLES = Path().getcwd().joinpath('runner', 'database', 'scripts', 'creating_tables')
PATH_TO_SCRIPTS_FOR_FILLING_TABLES = Path().getcwd().joinpath('runner', 'database', 'scripts', 'filling_tables')


def _get_script(path_to_script):
    return str(Path(path_to_script).lines())


def _execute_scripts_from_files(connection, path_to_scripts):
    for script in path_to_scripts:
        connection.executescript(_get_script(script))


def _create_database(conn):
    _execute_scripts_from_files(conn, PATH_TO_SCRIPTS_FOR_CREATING_TABLES.files('*.sql'))
    _execute_scripts_from_files(conn, PATH_TO_SCRIPTS_FOR_FILLING_TABLES.files('*.sql'))
    conn.commit()


def _fill_database(conn):
    cursor = conn.cursor()
    problem_downloaders = [TimusDownloader(), CodeforcesDownloader()]
    for downloader in problem_downloaders:
        problems, tags = downloader.get_problems_and_tags()
        for problem, tag in zip(problems, tags):
            insert_problem(cursor, problem, tag)
    conn.commit()


def get_training_set():
    db_is_exist = Path(PATH_TO_PROBLEM_DATABASE).exists()
    with sqlite_connect(PATH_TO_PROBLEM_DATABASE) as conn:
        if not db_is_exist:
            _create_database(conn)
            _fill_database(conn)
        return get_problems(conn)

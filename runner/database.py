from path import Path
from sqlite3 import connect as sqlite_connect


PATH_TO_PROBLEM_DATABASE = Path().getcwd().joinpath('database', 'problems.sqlite3')
PATH_TO_SCRIPTS_FOR_CREATING_TABLES = Path().getcwd().joinpath('database', 'scripts', 'creating_tables')
PATH_TO_SCRIPTS_FOR_FILLING_TABLES = Path().getcwd().joinpath('database', 'scripts', 'filling_tables')


def get_script(path_to_script):
    return "".join(Path(path_to_script).lines())


def execute_scripts_from_files(connection, path_to_scripts):
    for script in path_to_scripts:
        connection.executescript(get_script(script))


def create_database():
    connection_to_problems = sqlite_connect(PATH_TO_PROBLEM_DATABASE)
    execute_scripts_from_files(connection_to_problems, PATH_TO_SCRIPTS_FOR_CREATING_TABLES.files('*.sql'))
    execute_scripts_from_files(connection_to_problems, PATH_TO_SCRIPTS_FOR_FILLING_TABLES.files('*.sql'))


def get_learning_set():
    if not Path(PATH_TO_PROBLEM_DATABASE).exists():
        create_database()

import logging
from problem import Problem, Solution
import json


def deserialize_problems(fp):
    problems, tags = [], []

    try:
        default_obj = json.load(fp=fp)
        for problem_and_tags in default_obj:
            tmp_problem = problem_and_tags[0]
            tmp_tags = problem_and_tags[1]

            problem = Problem(statement=tmp_problem["statement"], link=tmp_problem["link"])
            problem.solutions = [Solution(solution["code"], solution["language"])
                                 for solution in tmp_problem["solutions"]]

            problems.append(problem)
            tags.append(tmp_tags)

    except (TypeError, KeyError) as e:
        logging.warning('Cannot deserialize problems')
        logging.exception(e)

    return problems, tags


def deserialize_problems_from_file(path_to_file):
    with open(path_to_file, "r") as f:
        return deserialize_problems(f)

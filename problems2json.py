import json
from problem import Problem, Solution


class ProblemEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Problem):
            return {"statement": o.statement, "link": o.link, "solutions": o.solutions}
        if isinstance(o, Solution):
            return {"language": o.language, "code": o.code}
        return json.JSONEncoder.default(self, o)


def serialize_problems(problems, tags, fp):
    to_serialize = list(zip(problems, tags))
    json.dump(to_serialize, fp, cls=ProblemEncoder, sort_keys=True)


def serialize_problems_to_file(problems, tags, path_to_file):
    with open(path_to_file, "w") as file:
        serialize_problems(problems, tags, file)

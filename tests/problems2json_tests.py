import unittest
from problem import Problem, Solution
from problems2json import serialize_problems, ProblemEncoder
from io import StringIO


class ProblemEncoderTest(unittest.TestCase):
    def setUp(self):
        self.problem_encoder = ProblemEncoder()

    def test_one_problem(self):
        problem = self.problem_encoder.default(Problem(statement='statement', link='link'))
        self.assertIsInstance(problem, dict)
        self.assertIn('statement', problem)
        self.assertIn('link', problem)
        self.assertEqual(problem['statement'], 'statement')
        self.assertEqual(problem['link'], 'link')

    def test_one_solution(self):
        solution = self.problem_encoder.default(Solution(code='code', language='language'))
        self.assertIsInstance(solution, dict)
        self.assertIn('code', solution)
        self.assertIn('language', solution)
        self.assertEqual(solution['code'], 'code')
        self.assertEqual(solution['language'], 'language')

    def test_problem_with_solution(self):
        solutions = [Solution(code='code1', language='language1')]
        problem = Problem(statement='statement', link='link', solutions=solutions)
        problem = self.problem_encoder.default(problem)
        self.assertIsInstance(problem, dict)
        self.assertIn('statement', problem)
        self.assertIn('link', problem)
        self.assertEqual(problem['statement'], 'statement')
        self.assertEqual(problem['link'], 'link')
        self.assertIn('solutions', problem)
        self.assertIsInstance(problem['solutions'], list)
        self.assertEqual(len(problem['solutions']), 1)
        self.assertIsInstance(problem['solutions'][0], Solution)


class Problems2JsonTest(unittest.TestCase):
    def test_one_problem_to_json(self):
        problems = [Problem('statement1', 'link1')]
        tags = [[]]
        f = StringIO()
        serialize_problems(problems, tags, f)
        self.assertEqual(f.getvalue(), '[[{"link": "link1", "solutions": [], "statement": "statement1"}, []]]')

    def test_one_problem_and_one_tag(self):
        problems = [Problem('statement1', 'link1')]
        tags = [[0]]
        f = StringIO()
        serialize_problems(problems, tags, f)
        self.assertEqual(f.getvalue(), '[[{"link": "link1", "solutions": [], "statement": "statement1"}, [1]]]')

if __name__ == '__main__':
    unittest.main()

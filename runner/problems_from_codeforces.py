import logging

from lxml.html import fromstring
import codeforces
from problem import Solution, Problem
from .problems_downloader_base import ProblemDownloaderBase


class CodeforcesDownloader(ProblemDownloaderBase):
    @staticmethod
    def _make_link_to_problem_statement(contest_id, index):
        return "http://codeforces.ru/problemset/problem/{0}/{1}".format(contest_id, index)

    @staticmethod
    def _make_link_to_submissions_list(contest_id, index, page):
        return "http://codeforces.com/problemset/status/{0}/problem/{1}/page/{2}?order=BY_PROGRAM_LENGTH_ASC". \
            format(contest_id, index, page)

    @staticmethod
    def _make_link_to_solution(contest_id, submission_id):
        return "http://codeforces.com/contest/{0}/submission/{1}".format(contest_id, submission_id)

    def _get_statement(self, link):
        content = fromstring(self.download_page(link))
        try:
            return " ".join([elem.text_content() for elem in content.xpath('//div[@class="problem-statement"]')[0]])
        except Exception as e:
            logging.warning('Unable to get problem statement from link={0}'.format(link))
            logging.exception(e)

    def _get_submission_ids_from_page(self, contest_id, index, page):
        allowed_c_languages = ('GNU C++', 'GNU C++11', 'MS C++')
        allowed_java_languages = ('Java 7', 'Java 8')
        submissions = []
        link = self._make_link_to_submissions_list(contest_id, index, page)
        content = fromstring(self.download_page(link))
        for elem in content.xpath('//*[@data-submission-id]'):
            lang = elem[4].text.strip()
            if lang in allowed_c_languages or lang in allowed_java_languages:
                submissions.append(
                    (
                        elem[0].xpath('a')[0].text.strip(),
                        Solution.cpp_lang if lang in allowed_c_languages else Solution.java_lang
                    )
                )
        return submissions

    def _get_submission_ids(self, contest_id, index, number_of_pages=1):
        submissions = []
        for page in range(1, number_of_pages + 1):
            submissions.extend(self._get_submission_ids_from_page(contest_id, index, page))
        return submissions

    def _get_solution(self, contest_id, submission_id):
        link = self._make_link_to_solution(contest_id, submission_id)
        content = fromstring(self.download_page(link))
        return content.xpath('//*[@class="prettyprint program-source"]')[0].text_content()

    def _get_solutions(self, contest_id, index):
        submission_ids = self._get_submission_ids(contest_id, index)
        return [Solution(self._get_solution(contest_id, submission_id), lang) for submission_id, lang in submission_ids]

    @staticmethod
    def _cf_tags2my_tags(cf_tags):
        cf_tags_to_my_tags = {
            "matrices": "math",
            "graph matchings": "flows",
            "probabilities": "math",
            "trees": "graph theory",
            "strings": "string algorithms",
            "2-sat": "graph theory",
            "two pointers": None,
            "dp": "dynamic programming",
            "number theory": "math",
            "divide and conquer": None,
            "binary search": None,
            "fft": None,
            "games": "game theory",
            "dsu": None,
            "chinese remainder theorem": "math",
            "expression parsing": "string algorithms",
            "hashing": "string algorithms",
            "graphs": "graph theory",
            "shortest paths": "shortest path",
            "greedy": "greedy",
            "math": "math",
            "schedules": None,
            "flows": "flows",
            "implementation": None,
            "sortings": None,
            "meet-in-the-middle": None,
            "ternary search": None,
            "bitmasks": None,
            "combinatorics": "math",
            "data structures": "data structures",
            "geometry": "geometry",
            "dfs and similar": "graph theory",
            "brute force": None,
            "constructive algorithms": None,
            "string suffix structures": "string algorithms"
        }
        return [cf_tags_to_my_tags[tag] for tag in cf_tags if cf_tags_to_my_tags.get(tag) is not None]

    def get_problems_and_tags(self):
        api = codeforces.CodeforcesAPI()
        cf_problems = api.problemset_problems()["problems"]

        problems = []
        tags = []
        for problem in cf_problems:
            link = self._make_link_to_problem_statement(problem.contest_id, problem.index)
            statement = self._get_statement(link)
            solutions = self._get_solutions(problem.contest_id, problem.index)
            problem_tags = self._cf_tags2my_tags(problem.tags)

            problems.append(Problem(statement, link, solutions))
            tags.append(problem_tags)

        return problems, tags

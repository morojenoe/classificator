from lxml.html import fromstring
from problem import Problem
from .problems_downloader_base import ProblemDownloaderBase


class TimusDownloader(ProblemDownloaderBase):
    @staticmethod
    def _make_link_to_table_of_problems(tag):
        return "http://acm.timus.ru/problemset.aspx?tag={0}".format(tag)

    @staticmethod
    def _get_link(problem_id):
        return 'http://acm.timus.ru/problem.aspx?num={0}&locale=en'.format(problem_id)

    def _get_problem_ids(self, tag):
        link = self._make_link_to_table_of_problems(tag)
        content = fromstring(self.download_page(link))
        return [elem[1].text for elem in content.xpath('//tr[@class="content"]') if elem[1].text.isdigit()]

    def _get_statement(self, link):
        content = fromstring(self.download_page(link))
        return content.xpath('//div[@class="problem_content"]')[0].text_content()

    def get_problems_and_tags(self):
        problems, tags = [], []

        tags_on_timus = ['structure', 'dynprog', 'game', 'geometry', 'graphs', 'numbers', 'string']
        name_tag = ['data structures', 'dynamic programming', 'game theory', 'geometry', 'graph theory', 'math',
                    'string algorithms']
        link2id = {}

        for index, tag in enumerate(tags_on_timus):
            print(tag)
            problem_ids = self._get_problem_ids(tag)
            for p_id in problem_ids:
                link = self._get_link(p_id)
                statement = self._get_statement(link)
                if link in link2id:
                    tags[link2id[link]].append(name_tag[index])
                else:
                    link2id[link] = len(tags)
                    problems.append(Problem(statement, link))
                    tags.append([name_tag[index]])

        return problems, tags

from abc import ABCMeta, abstractmethod
from urllib.request import urlopen
from urllib.error import URLError
import logging


class ProblemDownloaderBase(metaclass=ABCMeta):
    @staticmethod
    def download_page(link):
        try:
            return urlopen(link).read()
        except URLError as e:
            logging.warning('Unable to download page')
            logging.exception(e)

    @abstractmethod
    def get_problems_and_tags(self):
        raise NotImplementedError

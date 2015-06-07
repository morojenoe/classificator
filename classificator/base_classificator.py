from abc import ABCMeta, abstractmethod


class BaseACMClassificator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def fit(self, problems, tags):
        raise NotImplementedError

    @abstractmethod
    def predict(self, problems):
        raise NotImplementedError

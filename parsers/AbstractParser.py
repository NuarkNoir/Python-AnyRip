from abc import ABCMeta, abstractmethod


class AbstractParser:
    __metaclass__ = ABCMeta

    host = ""
    url_pattern = ""
    checker_regexp = ""
    links = []
    std_many_once = False

    def __init__(self, url):
        self.url = self._check_url(url)

    @abstractmethod
    def parse(self) -> list:
        """Распарсить и вернуть список изображений"""

    def _check_url(self, url):
        import re
        if not re.match(self.checker_regexp, url):
            raise Warning("Wrong url given! " + self.host + "parser requires '" + self.url_pattern + "' url pattern.")
        self._using(url)
        return url

    def _using(self, url):
        print(f"You are parsing content from {url} using parser for {self.host}")

    @staticmethod
    def log(inf, msg, fname="log.txt"):
        open(fname, "a+").write(msg + "\n")
        if inf:
            print(msg)
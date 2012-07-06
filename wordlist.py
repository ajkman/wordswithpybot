import re
import config

class WordList(object):
    def __init__(self):
        with open(config.wordfile, 'r') as f:
            contents = f.readlines()

        self._words = [w.strip() for w in contents]

    def check_word(self, word):
        return word in self._words

    def regex_search(self, pattern):
        regex = re.compile(pattern)
        return [w for w in self._words if regex.search(w) is not None]


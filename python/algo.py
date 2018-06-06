import sys


class algo:
    def add_rule(self, int, str):
        self.rules[int] = str

    def __init__(self, *args):
        self.rules = {}  # Dictionary
        for i in range(1, len(args), 2):
            if i >= len(args):
                break
            self.add_rule(args[i - 1], args[i])

    def __str__(self):
        ret = ""
        for key, value in self.rules.items():
            ret += (str(key) + " " + value + " ")
        return ret

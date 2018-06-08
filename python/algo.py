import sys


class algo:
    def __init__(self, *args):
        self.rules = {}  # Dictionary
        for rule in args:
            self.add_rule(rule)

    def add_rule(self, str):
        self.rules[str.count('0')] = str

    def __str__(self):
        ret = ""
        for key, value in self.rules.items():
            ret += (str(key) + " " + value + " ")
        return ret

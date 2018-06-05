import sys

class algo:
    def add_rule(self, int, str):
        self.rules[int] = str

    def __init__(self, *args):
        self.rules = {} #dictionary
        for i in range(1, len(args), 2):
            if i + 1 >= len(args): break
            self.add_rule(count_rule_1, rule_1)

    def __str__(self):
        for key,value in self.rules.items():
           sys.stdout.write(key + " " + value + " ")
        sys.stdout.write('\n')

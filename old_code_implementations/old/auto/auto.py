import os

with open("input3.txt") as f:
    for line in f:
        os.system("python3 idea.py " + line)

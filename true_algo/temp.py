import sys
import os


def readlines(filepath: str):
    with open(filepath) as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]
    return lines

lines = readlines(sys.argv[1])
for i,l in enumerate(lines):
    left, right = l.split(',')
    if right > left:
        print(i,l)

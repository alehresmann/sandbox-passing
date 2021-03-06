import sys
import os


def readlines(filepath: str):
    with open(filepath) as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]
    return lines

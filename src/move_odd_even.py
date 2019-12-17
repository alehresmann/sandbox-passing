import sys


def readlines(filepath: str):
    with open(filepath) as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]
    return lines


lines = readlines(sys.argv[1])
even = []
odd = []

for i in range(0, len(lines)):
    line = lines[i]
    if i % 2 == 0:
        even.append(line)
    else:
        odd.append(line)

[print(el) for el in even]
print("ODD")
[print(el) for el in odd]

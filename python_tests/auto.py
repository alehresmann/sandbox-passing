import os
import sys

with open(sys.argv[2]) as f:
    count = 0
    for line in f:
        sys.stderr.write("\rComputing line " + str(count))
        os.system("python3 " + sys.argv[1] + " " + line)
        count += 1

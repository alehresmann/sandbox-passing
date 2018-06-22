# script for calling some script on each line of a file. input: python3 auto.py [script] file

import os
import sys

with open(sys.argv[2]) as f:
    count = 0
    for line in f:
        sys.stderr.write("\rComputing line " + str(count))
        os.system("python3 " + sys.argv[1] + " " + line.strip('\n') + " 000111")
        count += 1

import logging
import sys
import random
from bitarray import bitarray
from committee import committee

def _shuffle(string):
    return ''.join(random.sample(string, len(string)))

def run_this_many_times(times: int, max_iterations: int):
    string_length = 32
    pattern_length = 4
    if string_length % pattern_length != 0:
        print('error with pattern length and string length!')

    for i in range(0, times):
        random_str = _shuffle('0' * int(string_length / 2) + '1' * int(string_length / 2))
        random_pattern = _shuffle('0' * int(pattern_length / 2) + '1' * int(pattern_length / 2))
        logging.info('attempting to reach pattern ' + random_pattern + ' from ' + random_str)

        run = committee(bitarray(random_str), bitarray(random_pattern), max_iterations)
        run.attach_new_bot(0,8)
        run.attach_new_bot(16,24)
        run.attach_new_bot(24,32)
        attempt = run.algorithm()
        if attempt == False:
            logging.warning('FAILED TO REACH ' + random_pattern + ' from ' + random_str +'. Perhaps try increasing the max iteration limit?')
            return
    logging.warning('all strings reached the pattern requested!')


def run_on_this_particular_input(inpt_string: str, pattern:str, max_iterations: int):
    run = committee(bitarray(inpt_string), bitarray(pattern), max_iterations)
    run.attach_new_bot(0,20)
    run.attach_new_bot(40,60)
    run.attach_new_bot(80,100)
    attempt = run.algorithm()
    if attempt == False:
        logging.warning('FAILED TO REACH ' + pattern + ' from ' + inpt_string +'. Perhaps try increasing the max iteration limit?')
        return

verbose = int(sys.argv[3])
if verbose == 0:
    logging.basicConfig(format='%(message)s', level=logging.WARNING)
elif verbose == 1:
    logging.basicConfig(format='%(message)s', level=logging.INFO)
elif verbose == 2:
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

run_this_many_times(int(sys.argv[1]), int(sys.argv[2]))
#run_on_this_particular_input(sys.argv[1], sys.argv[2], int(sys.argv[3]))

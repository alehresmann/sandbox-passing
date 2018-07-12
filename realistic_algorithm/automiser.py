import sys
import random
import logging

from bitarray import bitarray

from settings import settings


def _shuffle(string):
    return ''.join(random.sample(string, len(string)))

def run_this_many_times(times: int, string_length: int, pattern_length: int, max_iterations: int):
    if string_length % pattern_length != 0:
        print('error with pattern length and string length!')

    for i in range(0, times):
        random_str = _shuffle('0' * int(string_length / 2) + '1' * int(string_length / 2))
        random_pattern = _shuffle('0' * int(pattern_length / 2) + '1' * int(pattern_length / 2))
        logging.info('attempting to reach pattern ' + random_pattern + ' from ' + random_str)

        run = settings(bitarray(random_str), bitarray(random_pattern), max_iterations)
        run.assign_windows_to_robots()
        attempt = run.algorithm()
        if attempt == False:
            logging.warning('FAILED TO REACH ' + random_pattern + ' from ' + random_str +'. Perhaps try increasing the max iteration limit?')
            return
    logging.warning('all strings reached the pattern requested!')


def run_on_this_particular_input(inpt_string: str, pattern:str, max_iterations: int):
    run = settings(bitarray(inpt_string), bitarray(pattern), max_iterations)
    run.assign_windows_to_robots()
    attempt = run.algorithm()
    if attempt == False:
        logging.warning('FAILED TO REACH ' + pattern + ' from ' + inpt_string +'. Perhaps try increasing the max iteration limit?')
        return

verbose = int(sys.argv[5])
if verbose == 0:
    logging.basicConfig(format='%(message)s', level=logging.WARNING)
elif verbose == 1:
    logging.basicConfig(format='%(message)s', level=logging.INFO)
elif verbose == 2:
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

run_this_many_times(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
#run_on_this_particular_input(sys.argv[1], sys.argv[2], int(sys.argv[3]))

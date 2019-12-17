from bitarray import bitarray
from patterned_robot import robot
import sys
# O(w^2) for every iteration.
# way it works: every iteration, all robots do the following steps:
# 1. rearrange window to try and reach pattern.  # should be able to eliminate this step every iteration except after shuffling
# 2. look in sandbox and try to get

def _pairwise(it):  # used for assign_string_to_robots
    it = iter(it)
    while True:
        yield next(it), next(it)

def assign_string_to_robots(pattern: str, input_string: str):
    if len(input_string) % len(pattern) != 0:
        print('not a valid pattern length!')
        sys.exit(0)

    pattern = bitarray(pattern)
    input_list = []
    for i in range(0, len(input_string), len(pattern)):
        input_list.append(input_string[i : i + len(pattern)])
    robots = []
    robot_count = 0

    for window, sandbox in _pairwise(input_list):
        robot_count += 1
        robots.append(robot(pattern, bitarray(window), bitarray(sandbox), robot_count, int(len(input_list)/2)))
    return robots

def valid_string(robots):
    for rob in robots:
        if not rob.window == rob.pattern or not rob.sandbox == rob.pattern:
            return False
    return True

def print_robots(robots):
    ret = ''
    for rob in robots:
        ret += ' ' + str(rob)
    return ret

def algorithm(robots: list):  # list of robots
    iteration_count = 0

    print( str(iteration_count) +': ' + print_robots(robots))
    print('Preliminary step: rearranging window, sorting sandbox.')
    for rob in robots:  # O(r * w^2)
        rob.rearrange_window()
        rob.sandbox.sort()

    print( str(iteration_count) +': ' + print_robots(robots))


    print('starting...')

    while not valid_string(robots) and iteration_count < 100000:
        iteration_count += 1
        print( str(iteration_count) +': ' + print_robots(robots))

        print('rearranging from sandbox unless sandbox is pattern...')
        for rob in robots:
            if not rob.has_valid_sandbox():
                rob.rearrange_from_sandbox()
            elif not rob.has_valid_window():
                rob.randomise_count += 1
                if rob.randomise_count == rob.randomise_lim:
                    rob.randomise()
                    rob.randomise_count = 0
                    rob.has_randomised = True

        print( str(iteration_count) +': ' + print_robots(robots))

        print('swapping sandboxes and windows if needed...')
        for rob in robots:
            if rob.has_valid_window() and not rob.has_valid_sandbox():
                rob.rearrange_sandbox()
                if not rob.has_randomised:
                    rob.swap()
                else:
                    rob.has_randomised = False
        print( str(iteration_count) +': ' + print_robots(robots))

        print('passing sandboxes...')
        for rob in robots:
            robots[0].swap_sandboxes_with(rob)
        print( str(iteration_count) +': ' + print_robots(robots))

    if iteration_count == 100000:
        return False
    return True
def main(): #                                  '111111 000000 111000 000111 101010101010'
    robots = assign_string_to_robots(sys.argv[1], sys.argv[2])
    algorithm(robots)

#main()

from bitarray import bitarray
from general_robot import robot
import sys

def _pairwise(it):  # used for assign_string_to_robots
    it = iter(it)
    while True:
        yield next(it), next(it)

def split_input_string_to_robots(robot_num: int, input_string: str):
    if len(input_string) % robot_num != 0:
        print('not a valid robot quantity!')
        sys.exit(0)

    window_size = int( len(input_string) / (robot_num * 2))

    input_list = []
    for i in range(0, len(input_string), window_size):
        input_list.append(input_string[i : i + window_size])

    robots = []

    for i in range(0, len(input_list) - 1, 2):
        robots.append(robot(bitarray(input_list[i]), bitarray(input_list[i+1]), int(i / 2)))
    return robots

def assign_tasks_to_robots(output_string: str, robots: list):
    #if output_string % len(robots) != 0:
    #    extra = output_string[- (output_string % len(robots))]
    output_list = []
    for i in range(0, len(output_string), len(robots[0].window)):
        output_list.append(output_string[i : i + len(robots[0].window)])
    for i in range(0, len(robots)):
        robots[i].pattern = bitarray(output_list[ int(i)])

def valid_string(robots, expected_output: str):
    for rob in robots:
        if rob.window.to01() != expected_output[:len(rob.window)]:
            return False
        expected_output = expected_output[len(rob.window):]
        if rob.sandbox.to01() != expected_output[:len(rob.sandbox)]:
            return False
        expected_output = expected_output[len(rob.window):]
    return True

def print_robots(robots):
    ret = ''
    for rob in robots:
        ret += ' ' + str(rob)
    return ret

def pass_sandbox_to(rob_from, rob_mid, rob_to):  # used if rob_mid wants to keep his sandbox.
    rob_mid.swap_sandboxes_with(rob_from)
    rob_mid.swap_sandboxes_with(rob_to)
    rob_mid.swap_sandboxes_with(rob_from)

def algorithm(robots: list):  # list of robots
    iteration_count = 0

    print('starting...')
    while not valid_string(robots) and iteration_count < 1000:
        iteration_count += 1
        print(str(iteration_count) +': ' + print_robots(robots))

        print('rearranging in window...')
        for rob in robots:
            rob.rearrange_window()
        print(str(iteration_count) +': ' + print_robots(robots))

        print('rearranging from sandbox...')
        for rob in robots:
            rob.rearrange_from_sandbox()
        print( str(iteration_count) +': ' + print_robots(robots))

        print('swapping sandboxes and windows if needed...')
        for rob in robots:
            if rob.has_valid_window():
                rob.swap()
        print(str(iteration_count) +': ' + print_robots(robots))

        print('passing sandboxes...')
        for rob in robots:
            robots[0].swap_sandboxes_with(rob)
        print(str(iteration_count) +': ' + print_robots(robots))

def main():
    robots = split_input_string_to_robots(int(sys.argv[1]), sys.argv[2])
    output_string = sys.argv[3]
    assign_tasks_to_robots(output_string, robots)
    for r in robots:
        print(r)
        print(r.pattern.to01())
    #algorithm(robots)

main()

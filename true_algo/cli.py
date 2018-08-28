# verbosity levels:
#    minimal    = 0  , only prints successful algs
#    info       = 1  , also prints alg failure causes
#    debug      = 2  , also prints every round of every alg

import sys
import argparse
import logging
import random

from colorama import init

from configuration import configuration

def compute(config: str, pattern: str, pos_list: list, max_rounds: int, print_info: str, print_full: bool):
    try:
        int(pattern, 2)
        int(config, 2)
    except:
        raise AssertionError('You didn\'t give me binary strings for your pattern and/or your configuration!')

    if pattern.count('0') != int(config.count('0') / (len(config) / len(pattern))):
        raise AssertionError('Assure yourself you have the correct number of 1s and 0s in your config to reach the pattern!')

    if max_rounds < 1:
        raise AssertionError('Max rounds value must be greater than 1!')

    c = configuration(pattern, config, print_full)

    for pos in pos_list:
        c.attach_bot(pos)

    if 'c' in print_info:
        logging.warning('C_0:\n' + str(config))
    if 'p' in print_info:
        logging.warning('P:\n' + str(pattern))
    if 'a' in print_info:
        logging.warning(c.get_config_stats())
    if 'rou' in print_info:
        c.rounds_info = True

    c.run_algo(max_rounds)

    # printing extra info
    if 's' in print_info:
        logging.warning(c.get_robots_stats())
    if 'rob' in print_info:
        [logging.warning(bot) for bot in c.bots]


def main():
    parser = argparse.ArgumentParser(description='CLI for sandbox passing ' \
    'algorithm. Example input: python3 cli.py -v 2 -pi rc particular 000111 ' \
    '000000111111 1000 0')

    # verbosity
    parser.add_argument('--verbose', '-v', type=int, default=1,
            help='the verbosity of the output. 0, 1, or 2. Higher is more verbose. Default is 1.')

    parser.add_argument('--print_info', '-pi', default='',
            help='what you want to be printed as additional information. ' \
                    'Currently takes: \'c\' for configuration, \'p\' for ' \
                    'pattern, \'s\' for stats, \'r\' for robots. you can ' \
                    'use them in any order, eg: -pi scr')

    parser.add_argument('--print_full', '-pf', action='store_true',
            help='Whether or not you want the config to be printed fully ' \
                    'at every round or just minimally. You won\'t see a ' \
                    'change if verbosity is set to 0')
    # subparsers
    subparsers = parser.add_subparsers(title='subcommands - Use \'-h\' to find out more.',
    metavar='', dest='command')

    particular_parser = subparsers.add_parser('particular', help='For ' \
            'testing a particular input. Input: particular [pattern] ' \
            '[initial configuration] [max number of rounds] [bot start ' \
            'positions]\neg: particular 000111 000000000111111111 1000 0 12')

    random_parser = subparsers.add_parser('random', help='For testing ' \
            'random inputs. Input: [-p/-ps] [pattern or pattern size] ' \
            '[size of configuration] [max number of rounds] ' \
            '[number of robots] ' \
            '[number of random configurations generated] \neg: random ' \
            '-p 000111 60 1000 2 1')

    # particular
    particular_parser.add_argument('pattern', type=str, default='00001111',
            help = 'the pattern. Make sure it is a binary string.')

    particular_parser.add_argument('config', type=str, default='000000000000000000000000111111111111111111111111',
            help = 'the initial configuration. Make sure it is a binary string, and perfectly divisable by your pattern.')

    particular_parser.add_argument('max_rounds', type=int, default = 10000,
            help = 'the max number of rounds before the algo automatically stops and declares itself failed')

    particular_parser.add_argument('robot_starts', nargs='+', default = [0],
            help = 'the start positions of each robot. put a space between each position.')


    # random
    random_parser.add_argument('--pattern_size', '-ps', type=int,
            help = 'the pattern size.')

    random_parser.add_argument('--pattern', '-pa', type=str,
            help = 'the pattern size.')

    random_parser.add_argument('config_size', type=int, default=32,
            help = 'the configuration size. Make sure it is perfectly divisable by your pattern.')

    random_parser.add_argument('max_rounds', type=int, default = 10000,
            help = 'the max number of rounds before the algo automatically stops and declares itself failed')

    random_parser.add_argument('robots_quant', type=int, default=3,
            help = 'the number of robots. Will be randomly placed around the string.')

    random_parser.add_argument('config_quant', type=int, default=1,
            help = 'as its name suggests')


    # processing
    args = parser.parse_args()

    # verbose
    if args.verbose == 1:
        logging.basicConfig(format='%(message)s', level=logging.INFO)
    elif args.verbose == 2:
        logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(message)s', level=logging.WARNING)

    logging.warning(args)

    # running algo
    if args.command == 'particular':
        pos_list = [int(pos) for pos in args.robot_starts]
        compute(args.config, args.pattern, pos_list, args.max_rounds, args.print_info, args.print_full)

    elif args.command == 'random':
        if not args.pattern_size and not args.pattern:
            raise AssertionError('you need to give me a pattern (-p) or a pattern size (-ps) ! ')
            sys.exit(0)

        if args.pattern_size and args.config_size % args.pattern_size != 0:
            raise AssertionError('you didn\'t give a config size that divides perfectly into the pattern size!')
            sys.exit(0)

        for attempt in range(0, args.config_quant):
            if args.pattern_size:
                num_of_0s = random.randint(1, args.pattern_size - 1)
                pattern = ''.join(random.sample('0' * num_of_0s + '1' * (args.pattern_size - num_of_0s), args.pattern_size))
            elif args.pattern:
                pattern = args.pattern
            config = ''.join(random.sample(pattern * int(args.config_size / len(pattern)), args.config_size))
            pos_list = []
            for i in range(0, args.robots_quant):
                pos_list.append(i * len(pattern) * 2)
            compute(config, pattern, pos_list, args.max_rounds, args.print_info, args.print_full)


# don't call main unless the script is called directly.
if __name__ == '__main__':
    main()

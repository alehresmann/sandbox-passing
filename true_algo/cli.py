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


def main():
    parser = argparse.ArgumentParser(description='CLI for sandbox passing algos')

    # verbosity
    parser.add_argument('--verbose', '-v', type=int, default=0,
            help='the verbosity of the output. 0, 1, or 2.')

    parser.add_argument('--synchronise', '-s', action='store_true',
            help='whether or not robots are synchronised. Use when you have many robots relative to the config size.')

    # subparsers
    subparsers = parser.add_subparsers(title='subcommands - Use \'-h\' to find out more.',
    metavar='', dest='command')

    particular_parser = subparsers.add_parser('particular', help='For' \
            'testing a particular input. Input: particular [pattern]' \
            '[initial configuration] [max number of rounds] [bot start positions]')

    random_parser = subparsers.add_parser('random', help='For testing' \
            'randomg inputs. Input: [pattern size]' \
            '[size of configuration] [max number of rounds]' \
            '[number of robots]' \
            '[number of random configurations generated]')

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
    random_parser.add_argument('pattern_size', type=int, default=8,
            help = 'the pattern size.')

    random_parser.add_argument('config_size', type=int, default=32,
            help = 'the configuration size. Make sure it is perfectly divisable by your pattern.')

    random_parser.add_argument('max_rounds', type=int, default = 10000,
            help = 'the max number of rounds before the algo automatically stops and declares itself failed')

    random_parser.add_argument('robots_quant', type=int, default=3,
            help = 'the number of robots. Will be randomly placed around the string.')

    random_parser.add_argument('config_quant', type=int, default=1,
            help = 'as its name suggests')


    args = parser.parse_args()

    if args.verbose == 1:
        logging.basicConfig(format='%(message)s', level=logging.INFO)
    elif args.verbose == 2:
        logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(message)s', level=logging.WARNING)

    logging.warning(args)

    # processing
    if args.command == 'particular':
        try:
            int(args.pattern, 2)
            int(args.config, 2)
        except:
            logging.warning('you didn\'t give me binary strings for your pattern and/or your configuration!')
            sys.exit(0)

        if len(args.config) % len(args.pattern) != 0:
            logging.warning('you didn\'t give me binary strings for your pattern and/or your configuration!')
            sys.exit(0)

        if args.pattern.count('0') != int(args.config.count('0') / (len(args.config) / len(args.pattern))):
            logging.warning('assure yourself you have the correct number of 1s and 0s in your config to reach the pattern!')
            sys.exit(0)

        c = configuration(args.pattern, args.config)
        for pos in args.robot_starts:
            c.attach_bot(int(pos), args.synchronise)
        if args.synchronise:
            c.run_synchronised_algo(args.max_rounds)
        else:
            c.run_algo(args.max_rounds)
        c.print_robots_final()

    elif args.command == 'random':
        if args.config_size % args.pattern_size != 0:
            logging.warning('you didn\'t give a config size that divides perfectly into the pattern size!')
            sys.exit(0)
        num_of_0s = random.randint(1, args.pattern_size - 1)

        for attempt in range(0, args.config_quant):
            pattern = ''.join(random.sample('0' * num_of_0s + '1' * (args.pattern_size - num_of_0s), args.pattern_size))
            config = ''.join(random.sample(pattern * int(args.config_size / args.pattern_size), args.config_size))
            c = configuration(pattern, config)
            logging.warning(pattern)
            logging.warning(config)
            for i in range(0, args.robots_quant):
                c.attach_bot(i * args.pattern_size * 2, args.synchronise)

            if args.synchronise:
                c.run_synchronised_algo(args.max_rounds)
            else:
                c.run_algo(args.max_rounds)

            c.print_robots_final()

# don't call main unless the script is called directly.
if __name__ == '__main__':
    main()

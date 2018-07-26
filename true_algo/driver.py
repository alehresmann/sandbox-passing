import logging

from colorama import init

from configuration import configuration


verbose = 1 #int(sys.argv[3])
if verbose == 0:
    logging.basicConfig(format='%(message)s', level=logging.WARNING)
elif verbose == 1:
    logging.basicConfig(format='%(message)s', level=logging.INFO)
elif verbose == 2:
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)


init()  #colorama for printing coloured terminal output
c = configuration('000111', '000000000000000000000000000000000000111111111111111111111111111111111111')
c.attach_bot(0)
c.attach_bot(18)
c.attach_bot(30)
c.attach_bot(48)

c.run_algo(1000)
c.print_robots_final()

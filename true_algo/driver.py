import logging

from colorama import init

from committee import configuration


verbose = 2 #int(sys.argv[3])
if verbose == 0:
    logging.basicConfig(format='%(message)s', level=logging.WARNING)
elif verbose == 1:
    logging.basicConfig(format='%(message)s', level=logging.INFO)
elif verbose == 2:
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)


init()  #colorama
c = configuration('000111', '000000000000111111111111010101010101010101010101', 1000)
c.attach_bot(0, 0)
c.attach_bot(12,1)
c.run_algo()

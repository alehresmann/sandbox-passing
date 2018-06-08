import generators
from configuration import configuration, configuration_builder
import test_algorithm as ta

def test_all_algorithms(pattern: str):
    # tests all algorithms of length [length]
    cb = configuration_builder()
    all_algs = generators.generate_all_algorithms(2,len(pattern));
    for alg in all_algs:
        max_iterations = 10000
        verbose = False
        # testing on the string of form 0+1+
        string = '0'* len(pattern) * 5 + '1' * len(pattern) * 5
        committee = (string, pattern)
        conf = cb.with_alg(alg)
        .with_pattern(pattern)
        .with_committee(committee)
        .with_max_iterations(mrakax_iterations)
        .with_verbose(verbose)
        .build()
        ta.linear_algorithm(conf)

        for i in range(0, 

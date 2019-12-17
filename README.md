# Sandbox Passing

# Table of Contents
* **What is this ?**
* **Requirements and Installation**
* **Why This Utility?**
* **Brief Usage**
* **Preliminary Options**
* **Running the Algorithm**
* **Particular Input**
* **Random Input**


# What is this ?
The following repository contains code written during my bachelor's at Concordia University, which eventually resulted in the publication "Distributed Pattern Formation in a Ring" in [SIROCCO 2019](https://cs.gssi.it/sirocco2019/), [available on axiv.org](https://arxiv.org/abs/1905.08856). I highlight that the code is rather old and shows a clear lack of experience in both good programming as well as research practices. Nevertheless, the last implementation is quite useable, and thus perhaps worth putting it online. I highly doubt anyone will even read it, but for the sake of "open science" and archival purposes, I publish it here.

The folder *src* contains the final implementation that was used for this project. the folder *old_code_implementations* contains, as it suggests, various implementations of the problem in different forms: most are probably only halfway implemented or/and have bugs, so I highly recommend not looking at them.

For any questions, I am reachable at al at ehresmann dot eu.

# Requirements:
* python3.6+
* bitarray: install with pip: `pip install bitarray`
* colorama: install with pip: `pip install colorama`

# Why This Utility?
We sought to make a distributed algorithm for the problem described in "Satisfying Neighbor Preferences in a Circle" by Krizanc et al.

# Brief Usage:

`python3 cli.py [-v=<k>] [-pi=<str>] [-pf] [-ia] random|particular [...]`

# Preliminary Options:

`-v | --verbose <k>`

For specifying verbosity. `k` can be 0, 1, or 2.

* 0: don't print anything except whether or not the algorithm succeeded, and errors.
* 1: print every iteration. This is the default option if verbosity isn't specified.
* 2: print the actions of each robot on every iteration

`-pi | --print_info <str>`

For specifying any additional information to be printed. May be in conflict with verbosity, so be sure to have verbosity at least 1. You can give any of the following in any order, as long as you have them in a single string, e.g.: -pi csrour

* c: Prints the initial configuration. Useful for when you want to run the random algorithm with verbosity 0, but still need to know the input configuration used.
* `p`: Prints the pattern sought out. Once again, useful when one uses the random algorithm.
* `a`: Prints the analyser output, a.k.a get the bound of the input.
* `rou`: Prints round info, a.k.a number of invalid slices at each round. Useful when one uses the analyser.
* `s`: Prints statistics of each robot after the algorithm was run, such as number of moves, number of bits swapped, when the robot finished, etc.
* `rob`: Prints information of the robot. Useful pretty much only in development.

`-pf | --print_full`

For seeing the actual algorithm at play on each slice, not just whether a slice is valid, patterned, or zero/one-heavy. Informative but dense to read.

`-ia | --ignore_analyser`

For preventing the analyser from verifying that the bound is met at every pass, in case one wants to rush computations.

# Running the Algorithm

### Particular Input

When one wants to run the algorithm on particular input, one should use the `particular` command. This takes in a specific input configuration, pattern, and robot placement, and returns the result of the algorithm using the specified input. Useful for precise testing.

Usage: `python3 cli.py [preliminary options...] particular [pattern] [initial configuration] [max number of rounds] [bot start positions]`

eg: `python3 cli.py -pf particular 000111 000000000111111111 1000 0 12`

The above runs the algorithm on the initial configuration `000000000111111111`, seeks to reach the pattern `000111`, has a maximum number of rounds of 1000 before it stops, and has two robots, one whose window starts on slice 0, the other whose window starts on slice 12.

### Random Input

When you instead want to look at the behaviour of the algorithm in a more general manner, use random input. You may specify a random configuration with a specific pattern, or a random configuration and a random pattern. For now, all robots are placed next to each other.

Usage: `python3 cli.py [preliminary options...] random [(-p/--pattern <str> )|(--pattern_size <int>)] [initial configuration] [max number of rounds] [number of robots] [number of runs to attempt]`

eg: `python3 cli.py -pf random -pz 6 60 1000 2 1`

The above runs the algorithm on a single random configuration of size 60, attempting to reach a random pattern, using two robots.

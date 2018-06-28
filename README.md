# Schelling Utility

# Table of Contents
* **Requirements and Installation**
* **Brief Usage**
* **Examples**
* **Notes on the design and the implementations**

# Requirements:
* python3.6+
* bitarray: install with `pip3 install bitarray`


# Brief Usage:

`python3 cli.py [pattern] [input_string options] [algorithms options] [extra configurations]`

### pattern:
Some binary string to be reached by the algorithms.

Example: `000111`

### input_string options:

You may give input strings in a few different manners:

1. *Directly inputting a static input string*:

`-i [input string]`

Example: `-i 000000111111`

2. *Generating a number of random strings of particular size*:

`-m [multiplier] -rs [number of random strings to generate]`

Example: `-m 5 -rs 1000`
This generates 1000 random strings of size 5 * (length of pattern)

3. *Feeding a file containing one string at every line*

`-sf [string file]`

Example: `-sf strings_to_test.txt`

### algorithms options
You may also give algorithms in a few different manners:

1. Directly inputting a static algorithm

`-a [rules]`

Example: `-a 000111 001010 110100`

2. Generating a number of random algorithms with a particular number of rules.

`-nra [num of rand algorithms to generate] -nr [num of rules per each algorithm]`

Example: `-nra 1000 -nr 2`

3. Generating all possible algorithms with a number of rulese in particular.

`-all -nr [number of rules per each algorthim]`

Example: `-all -nr 2`

### Configuration Options
Finally, you may alter a few parameters in the configuration. Each of these can be used concurrently, unlike the options detailed above.

1. verbose

`-v`

This turns on verbose mode, printing out details about the way the program is behaving.

2. max iterations

This modifies the number of iterations an algorithm is allowed to go through before it is declared as having failed.

`-mi [max iterations]`

Example: `-mi 10000`

3. no cycles

`-nc`

This turns off cycle detection, allowing the iterations to sometimes return to some previous configuration. This is less taxing on memory, but may cycle and thus waste computing power.

# Examples

Suppose I initially wish to figure out which algorithms work with two rules, on the pattern `00001111`. First, I test all algorithms on a reasonable amount of strings:

`python3 cli.py 00001111 -m 5 -rs 1000 -all -nr 2 -mi 10000`

From this, I extract all the algorithms that did work, and write them in a file named `algs_that_work_length_8.txt`.

I want to verify whether or not these algorithms work on input strings of larger sizes:

`python3 cli.py 00001111 -m 20 -rs 1000 -af algs_that_work_length_8.txt -mi 10000`

I  find that none of them work. Intrigued, I test the first algorithm and verify whether or not it reaches valid configuration when not checking for cycles.

`python3 cli.py 00001111 -m 20 -rs 1000 -a  -mi 100000 -v -nc`

# Notes on the Design and the Implementation

TODO

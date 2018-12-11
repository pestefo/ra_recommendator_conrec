#!/usr/bin/env python
# coding: utf-8

'''
Get a frequency of pairs from a lists of elements
-------------------------------------------------

Ex. 
1,2,3
1,2
1,2
1,2,3,4

-->

1,2 -> 4
1,3 -> 2
1,4 -> 1
2,3 -> 2
2,4 -> 1
3,4 -> 1
'''

import itertools


def increment_dict(dictionary, pairs):

    for pair in pairs:

        if pair in dictionary:
            dictionary[pair] += 1
        else:
            dictionary[pair] = 1


def print_nodes(nodes):
    pass

def print_edges(dictionary):
	pass


def main():

    path_to_file = 'example.txt'
    separator = ','
    pairs_dict = {}
    nodes = set()

    with open(path_to_file) as data:
        for line in data:
            elements = line.rstrip().split(separator)
            if len(elements) >= 2:
                nodes = nodes.union(set(elements))

                pairs = [i for i in itertools.combinations(elements, 2)]
                increment_dict(pairs_dict, pairs)

    print(nodes)
    print(pairs_dict)


if __name__ == '__main__':
    main()

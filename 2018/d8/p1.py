from collections import defaultdict, deque, namedtuple
import re
import math
from heapq import *
import itertools

Node = namedtuple('Node', ['children', 'meta'])


def parse(filename):
    data = list(map(int, open(filename).read().split(' ')))
    return data


def build_tree(data):
    node, nc, nm, data = Node([], []), data[0], data[1], data[2:]
    for _ in range(nc):
        c, data = build_tree(data)
        node.children.append(c)
    node.meta.extend(data[0:nm])
    data = data[nm:]

    return node, data


def sum_metadata1(node):
    total = sum(node.meta)
    for c in node.children:
        total += sum_metadata1(c)
    return total


def sum_metadata2(node):
    if not node.children:
        return sum(node.meta)
    return sum(sum_metadata2(node.children[c - 1]) for c in node.meta if c <= len(node.children))


def part1(data):
    print(sum_metadata1(build_tree(data)[0]))


def part2(data):
    print(sum_metadata2(build_tree(data)[0]))


data = parse("input")
part1(data)
part2(data)

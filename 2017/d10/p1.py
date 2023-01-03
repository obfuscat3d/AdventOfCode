import re
from itertools import *
from functools import *


def chunk(l, n):
    cs = len(l) // n
    return [l[cs * i:cs * i + cs] for i in range(n)]


def knot_round(R, pos, skip_size, lengths):
    S = len(R)
    for flip_len in lengths:
        a, b = pos, pos + flip_len - 1
        while a < b:
            R[a % S], R[b % S], a, b = R[b % S], R[a % S], a + 1, b - 1
        pos, skip_size = (pos + skip_size + flip_len) % S, skip_size + 1
    return R, pos, skip_size


def knot_hash(key):
    lengths = list(map(ord, key)) + [17, 31, 73, 47, 23]
    R, pos, skip_size = list(range(256)), 0, 0
    for _ in range(64):
        R, pos, skip_size = knot_round(R, pos, skip_size, lengths)
    chunks = map(lambda x: reduce(lambda a, b: a ^ b, x, 0), chunk(R, 16))
    hex_vals = map(lambda x: "{:02x}".format(x), chunks)
    return ''.join(hex_vals)


def part1():
    lengths = list(map(int, re.findall("\d+", open("input").read())))
    R, _, _ = knot_round(list(range(256)), 0, 0, lengths)
    print(R[0] * R[1])


def part2():
    print(knot_hash(open("input").read()))


part1()
part2()

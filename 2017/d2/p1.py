from itertools import *
import re

data = [list(map(int, re.findall("\d+", l))) for l in open("input").read().split('\n')]
print(sum((b - a) for a, *_, b in map(sorted, data)))
print(sum(a // b for l in data for a, b in permutations(l, 2) if a % b == 0))

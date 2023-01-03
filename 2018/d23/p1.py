import re
from z3 import *


def md3(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def parse(filename):
    bots = []
    for l in open(filename).read().split('\n'):
        x, y, z, r = re.findall("-?\d+", l)
        bots.append(tuple(map(int, (x, y, z, r))))
    return bots


def part1(bots):
    p = sorted(bots, key=lambda x: x[3])[-1]
    print(len([1 for b in bots if md3(p, b) <= p[3]]))


def part2(bots):
    o = Optimize()
    x, y, z = Int('x'), Int('y'), Int('z')
    ir = [Int("ir" + str(i)) for i, _ in enumerate(bots)]
    total = Int("total")
    dist = Int("dist")
    for i, (x0, y0, z0, r) in enumerate(bots):
        o.add(ir[i] == If(Abs(x0 - x) + Abs(y0 - y) + Abs(z0 - z) <= r, 1, 0))
    o.add(total == Sum(ir))
    o.add(dist == Abs(x) + Abs(y) + Abs(z))
    o.maximize(total)
    o.minimize(dist)
    o.check()
    print(o.model()[dist])


bots = parse("input")
part1(bots)
part2(bots)

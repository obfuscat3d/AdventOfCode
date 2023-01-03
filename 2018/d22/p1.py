from collections import namedtuple
import re
from heapq import *


def parse(filename):
    text = open(filename).read().split('\n')
    depth = int(re.findall("\d+", text[0])[0])
    x, y = re.findall("\d+", text[1])
    return depth, int(x) + 1j * int(y)


def part1(depth, target):
    gi, el, terrain = {}, {}, {}
    for x in range(0, int(target.real) + 120):
        for y in range(0, int(target.imag) + 120):
            p = x + 1j * y
            if x == 0:
                gi[p] = 48271 * y
                el[p] = (gi[p] + depth) % 20183
            elif y == 0:
                gi[p] = 16807 * x
                el[p] = (gi[p] + depth) % 20183
            else:
                gi[p] = el[p - 1] * el[p - 1j]
                el[p] = (gi[p] + depth) % 20183

            if p == target:
                gi[p] = 0
                el[p] = depth

            terrain[p] = el[p] % 3

    print(sum(v for k, v in terrain.items() if k.real <= target.real and k.imag <= target.imag))
    return terrain


ROCK, WET, NARROW, CLIMBING, TORCH, NEITHER = 0, 1, 2, 10, 11, 12
ALLOWED = {
    ROCK: {CLIMBING, TORCH},
    WET: {CLIMBING, NEITHER},
    NARROW: {TORCH, NEITHER}
}


State = namedtuple('State', ['d', 'inc', 'p', 'equip'])


def part2(terrain, target):
    inc, queue, min_depth = 1, [State(0, 0, 0, TORCH)], {0: 0}
    while queue:
        c = heappop(queue)
        # print(c)
        if c.p == target:
            print(c.d)
            return
        for n in [c.p - 1j, c.p - 1, c.p + 1, c.p + 1j]:
            if n not in terrain:
                continue
            for e in (ALLOWED[terrain[n]] if n != target else [TORCH]):
                if (n, e) in min_depth:
                    if min_depth[(n, e)] <= c.d + (1 if e == c.equip else 8):
                        continue
                min_depth[(n, e)] = c.d + (1 if e == c.equip else 8)
                inc += 1
                heappush(queue, State(c.d + (1 if e == c.equip else 8), inc, n, e))


depth, target = parse("input")
terrain = part1(depth, target)
part2(terrain, target)

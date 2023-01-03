import re
from z3 import *


def manhattan_distance(x0, y0, x1, y1):
    return abs(x0 - x1) + abs(y0 - y1)


def get_sensor_data(filename):
    return [list(map(int, re.findall("-?\d+", line))) for line in open(filename).read().split('\n')]


def part1(sensor_data):
    Y_COORD, not_beacon = 2_000_000, set()
    for sx, sy, bx, by in sensor_data:
        d = manhattan_distance(sx, sy, bx, by)
        d2 = abs(sy - Y_COORD)
        not_beacon.update(range(sx - d + d2, sx + d - d2))
    print(len(not_beacon))


def part2(sensor_data):
    x, y, solution = Int('x'), Int('y'), Int('solution')
    s = Solver()
    for a in [solution == 4_000_000 * x + y, x > 0, x < 4_000_000, y > 0, y < 4_000_000]:
        s.add(a)
    for sx, sy, bx, by in sensor_data:
        d = manhattan_distance(sx, sy, bx, by)
        s.add(Abs(sx - x) + Abs(sy - y) > d)
    s.check()
    print(s.model())


sensor_data = get_sensor_data('input')
part1(sensor_data)
part2(sensor_data)

import re
import collections


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


def is_covered_by_sensors(sensor_data, x, y):
    for sx, sy, bx, by in sensor_data:
        if manhattan_distance(sx, sy, x, y) <= manhattan_distance(sx, sy, bx, by):
            return True
    return False


def get_candidates_for_beacon(sensor_data, boundary):
    candidates = collections.Counter()
    for sx, sy, bx, by in sensor_data:
        dist = manhattan_distance(sx, sy, bx, by)
        for i in range(dist):
            if 0 <= sx - dist + i - 1 <= boundary and 0 <= sy + i <= boundary:
                candidates[(sx - dist + i - 1, sy + i)] += 1

            if 0 <= sx - dist + i + 1 <= boundary and 0 <= sy - i <= boundary:
                candidates[(sx - dist + i + 1, sy - i)] += 1

            if 0 <= sx + i <= boundary and 0 <= sy - dist - i - 1 <= boundary:
                candidates[(sx + i, sy - dist - i - 1)] += 1

            if 0 <= sx - i <= boundary and 0 <= sy - dist + i + 1 <= boundary:
                candidates[(sx - dist + i + 1, sy - i)] += 1
    return candidates


def part2(sensor_data):
    candidates = get_candidates_for_beacon(sensor_data, 4_000_000)
    for x, y in [p for p, _ in candidates.most_common()]:
        if not is_covered_by_sensors(sensor_data, x, y):
            print(x, y, 4_000_000 * x + y)
            return


sensor_data = get_sensor_data('input')
part1(sensor_data)
part2(sensor_data)

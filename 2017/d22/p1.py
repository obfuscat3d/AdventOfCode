from copy import deepcopy


def parse(filename):
    grid = {}
    for y, line in enumerate(open(filename).read().split('\n')):
        for x, c in enumerate(line):
            grid[x + 1j * y] = c
    return grid


def part1(start, data):
    p, dp, score = start, -1j, 0
    for _ in range(10000):
        if data.get(p, '.') == '#':
            data[p], dp = '.', dp * 1j
        elif data.get(p, '.') == '.':
            score, data[p], dp = score + 1, '#', dp * -1j
        p += dp
    print(score)


def part2(start, data):
    # 0 clean, 1 weak, 2 infected, 3 flagged
    data = {k: 0 if v == '.' else 2 for k, v in data.items()}
    p, dp, score = start, -1j, 0
    for _ in range(10000000):
        if data.get(p, 0) == 0:
            data[p], dp = 1, dp * -1j
        elif data.get(p, 0) == 1:
            data[p], score = 2, score + 1
        elif data.get(p, 0) == 2:
            data[p], dp = 3, dp * 1j
        elif data.get(p, 0) == 3:
            data[p], dp = 0, dp * -1
        p += dp
    print(score)


data = parse("input")
START = 12 + 12j
part1(START, deepcopy(data))
part2(START, deepcopy(data))

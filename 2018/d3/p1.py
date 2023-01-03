import re
from collections import defaultdict


def parse(filename):
    text = open(filename).read().split('\n')
    regions = [list(map(int, re.findall("\d+", l))) for l in text]
    grid = defaultdict(int)
    for _, a, b, c, d in regions:
        for x in range(a, a + c):
            for y in range(b, b + d):
                grid[x + 1j * y] += 1
    return regions, grid


def part1(grid):
    print(len([1 for v in grid.values() if v > 1]))


def part2(regions, grid):
    for q, a, b, c, d in regions:
        good = True
        for x in range(a, a + c):
            for y in range(b, b + d):
                if grid[x + 1j * y] > 1:
                    good = False
        if good:
            print(q)


regions, grid = parse("input")
part1(grid)
part2(regions, grid)

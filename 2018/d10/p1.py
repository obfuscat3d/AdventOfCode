import re


def parse(filename):
    lines = open(filename).read().split('\n')
    return [list(map(int, re.findall("-?\d+", l))) for l in lines]


def print_grid(grid):
    min_x = min(p[0] for p in grid)
    max_x = max(p[0] for p in grid)
    min_y = min(p[1] for p in grid)
    max_y = max(p[1] for p in grid)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in grid:
                print("#", end="")
            else:
                print(" ", end="")
        print()
    print()


def part1(data):
    i = 1
    best_grid, low_y_diff, best_i = None, 1 << 32, 0
    while i < 12000:
        for p in data:
            p[0] += p[2]
            p[1] += p[3]
        grid = {(p[0], p[1]) for p in data}
        min_y = min(p[1] for p in grid)
        max_y = max(p[1] for p in grid)
        if max_y - min_y < low_y_diff:
            best_grid, low_y_diff, best_i = grid, max_y - min_y, i
        i += 1

    print_grid(best_grid)
    print(best_i)


data = parse("input")
part1(data)

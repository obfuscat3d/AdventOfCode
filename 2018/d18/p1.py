from collections import defaultdict


def parse(filename):
    text = open(filename).read()
    lines = text.split('\n')
    grid = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            grid[x + 1j * y] = c

    return grid


def neighbor_tiles(grid, p):
    tiles = defaultdict(int)
    for p1 in [p - 1, p + 1, p - 1j, p + 1j, p - 1 + 1j, p - 1 - 1j, p + 1 - 1j, p + 1 + 1j]:
        if p1 in grid:
            tiles[grid[p1]] += 1
    return tiles


def step(grid):
    new_grid = {}
    for p, v in grid.items():
        n = neighbor_tiles(grid, p)
        if v == '.':
            new_grid[p] = '|' if n['|'] >= 3 else '.'
        elif v == '|':
            new_grid[p] = '#' if n['#'] >= 3 else '|'
        elif v == '#':
            new_grid[p] = '#' if n['#'] >= 1 and n['|'] >= 1 else '.'
        else:
            assert False, "shouldn't get here"
    return new_grid


def resource_value(grid):
    wooded = len([1 for k, v in grid.items() if v == '|'])
    lumberyard = len([1 for k, v in grid.items() if v == '#'])
    return wooded * lumberyard


def part1(grid):
    for _ in range(10):
        grid = step(grid)
    print(resource_value(grid))


def part2(grid):
    seen_l, rv, i = [], None, 0
    while True:
        rv = resource_value(grid)
        if rv in seen_l:
            idx = seen_l.index(rv)
            seen_l.append(rv)
            # Three in a row to indicate pattern? Seems legit
            if seen_l[-3:] == seen_l[idx - 2:idx + 1]:
                break
        else:
            seen_l.append(rv)

        grid = step(grid)
        i += 1

    idx = seen_l.index(seen_l[-1])
    interval = len(seen_l) - idx - 1
    print(seen_l[idx + ((1000000000 - idx) % interval)])


data = parse("input")
part1(data)
part2(data)

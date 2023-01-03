from types import SimpleNamespace
from copy import deepcopy


def Cart(p, dp, turn=0, crashed=False):
    return SimpleNamespace(p=p, dp=dp, turn=turn, crashed=crashed)


def parse(filename):
    lines = open(filename).read().split('\n')
    carts, grid = [], {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c in ['|', '/', '-', '\\', '+']:
                grid[x + 1j * y] = c
            elif c != ' ':
                DIRS = {'^': -1j, '>': 1, '<': -1, 'v': 1j}
                PIECE = {'^': '|', '>': '-', '<': '-', 'v': '|'}
                grid[x + 1j * y] = PIECE[c]
                carts.append(Cart(x + 1j * y, DIRS[c]))
    return carts, grid


def step(carts, grid):
    crashes = []
    for c in sorted(carts, key=lambda c: 1000 * c.p.imag + c.p.real):
        if c.crashed:
            continue

        c.p += c.dp

        for c1 in carts:
            if c.p == c1.p and c != c1 and not c1.crashed and not c.crashed:
                c.crashed = c1.crashed = True
                crashes.extend([c, c1])
                break
        else:
            if grid[c.p] == '/':
                c.dp = -c.dp.imag - 1j * c.dp.real
            elif grid[c.p] == '\\':
                c.dp = c.dp.imag + 1j * c.dp.real
            elif grid[c.p] == '+':
                turn_ops = [lambda p: p.imag - 1j * p.real,   # left
                            lambda p: p,                      # straight
                            lambda p: -p.imag + 1j * p.real]  # right
                c.dp = turn_ops[c.turn % len(turn_ops)](c.dp)
                c.turn += 1

    for c in crashes:
        carts.remove(c)
    return crashes


def part1(carts, grid):
    crashes = None
    while not crashes:
        crashes = step(carts, grid)
    print(crashes[0].p)


def part2(carts, grid):
    while len(carts) > 1:
        _ = step(carts, grid)
    print(carts[0].p)


carts, grid = parse("input")
part1(deepcopy(carts), grid)
part2(deepcopy(carts), grid)

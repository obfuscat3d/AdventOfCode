import string


def parse(filename):
    T = open(filename).read().split('\n')
    return {x + 1j * y: c for y, L in enumerate(T) for x, c in enumerate(L) if c != ' '}


def part1and2(grid):
    start = min(grid.keys(), key=lambda p: p.imag)
    p, dp, steps, answer = start, 1j, 0, ""
    while p in grid:
        if grid[p] in string.ascii_letters:
            answer += grid[p]
        elif grid[p] == '+':
            dp *= -1j if p + dp * -1j in grid else 1j
        steps, p = steps + 1, p + dp

    print(answer)
    print(steps)


part1and2(parse("input"))

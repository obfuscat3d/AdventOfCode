"""
Utility j0nx.
"""


def argmax(l):
    """Negative indicies so the first occurance of a value is returned."""
    return -max((x, -i) for i, x in enumerate(l))[1]


def argmin(l):
    """Negative indicies so the first occurance of a value is returned."""
    return -min((x, -i) for i, x in enumerate(l))[1]


def chunk(l, n):
    """n = number of chunks, not size of chunk"""
    assert len(l) % n == 0
    cs = len(l) // n
    return [l[cs * i:cs * i + cs] for i in range(n)]


def slurp_grid(filename):
    """Read a grid from a file. TODO: take in the text here instead of filename?"""
    grid = {}
    for y, line in enumerate(open(filename).read().split('\n')):
        for x, c in enumerate(line):
            grid[x + 1j * y] = c
    return grid


def pg(grid):
    """Basic grid-printing function"""
    ys = sorted(int(p.imag) for p in grid.keys())
    xs = sorted(int(p.real) for p in grid.keys())
    for y in range(ys[0], ys[-1] + 1):
        for x in range(xs[0], xs[-1] + 1):
            print(grid[x + 1j * y], end="")
        print()
    print()


def n4(p):
    return [p - 1j, p - 1, p + 1, p + 1j]


def n8(p):
    return [p - 1 - 1j, p - 1j, p + 1 - 1j, p - 1, p + 1, p - 1 + 1j, p + 1j, p + 1 + 1j]


def md(a, b):
    """Manhattan distance for arbitrary dimension tuples"""
    return sum(map(abs, [i - j for i, j in zip(a, b)]))


def mdc(a, b):
    """Manhattan distance for complex coordinates"""
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))


def ulam_spiral(max_num):
    """
        Returns two values:
         - a dict of number -> complex coordinate
         - a dict of coordinate -> number
    """
    address, v, p, edge_size = {1: 0}, 2, 1, 2
    while v <= max_num:
        for _ in range(edge_size - 1):
            address[v], p, v = p, p - 1j, v + 1
        for _ in range(edge_size):
            address[v], p, v = p, p - 1, v + 1
        for _ in range(edge_size):
            address[v], p, v = p, p + 1j, v + 1
        for _ in range(edge_size + 1):
            address[v], p, v = p, p + 1, v + 1
        edge_size += 2
    return address, {v: k for k, v in address.items()}

"""
Note: the input here is small enough to brute force. Part 1 could be 
optimized by looking at the odd-squares on the bottom left corners and
starting from the nearest square under our target. But... calculating
the whole grid is pretty trivial here.
"""


def mdc(a, b):
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))


def n8(p):
    return [p - 1 - 1j, p - 1j, p + 1 - 1j, p - 1, p + 1, p - 1 + 1j, p + 1j, p + 1 + 1j]


def part1(data):
    address, v, p, edge_size = {1: 0}, 2, 1, 2
    while v <= data:
        for _ in range(edge_size - 1):
            address[v], p, v = p, p - 1j, v + 1
        for _ in range(edge_size):
            address[v], p, v = p, p - 1, v + 1
        for _ in range(edge_size):
            address[v], p, v = p, p + 1j, v + 1
        for _ in range(edge_size + 1):
            address[v], p, v = p, p + 1, v + 1
        edge_size += 2

    print(mdc(address[data], 0))


def part2(data):
    grid, p, edge_size = {0: 1}, 1, 2
    while True:
        for _ in range(edge_size - 1):
            if (q := sum(grid.get(c, 0) for c in n8(p))) > data:
                print(q)
                return
            grid[p], p = q, p - 1j
        for _ in range(edge_size):
            if (q := sum(grid.get(c, 0) for c in n8(p))) > data:
                print(q)
                return
            grid[p], p = q, p - 1
        for _ in range(edge_size):
            if (q := sum(grid.get(c, 0) for c in n8(p))) > data:
                print(q)
                return
            grid[p], p = q, p + 1j
        for _ in range(edge_size + 1):
            if (q := sum(grid.get(c, 0) for c in n8(p))) > data:
                print(q)
                return
            grid[p], p = q, p + 1
        edge_size += 2


data = 312051
part1(data)
part2(data)

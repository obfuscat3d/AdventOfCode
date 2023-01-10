from itertools import *


def neighbors(layer_pos):
    layer, p = layer_pos
    for c in [(layer, p - 1j), (layer, p - 1), (layer, p + 1), (layer, p + 1j)]:
        yield c
    if p.real == 0:
        yield (layer - 1, 1 + 2j)
    if p.real == 4:
        yield (layer - 1, 3 + 2j)
    if p.imag == 0:
        yield (layer - 1, 2 + 1j)
    if p.imag == 4:
        yield (layer - 1, 2 + 3j)
    if p == 1 + 2j:
        for i in range(5):
            yield (layer + 1, 1j * i)
    if p == 2 + 1j:
        for i in range(5):
            yield (layer + 1, i)
    if p == 3 + 2j:
        for i in range(5):
            yield (layer + 1, 4 + 1j * i)
    if p == 2 + 3j:
        for i in range(5):
            yield (layer + 1, i + 4j)


def step(grid, round):
    new_grid = {}
    for layer, x, y in product(range(-round - 1, round + 2), range(5), range(5)):
        if x != 2 or y != 2:
            p = (layer, x + 1j * y)
            temp = sum(grid.get(n, 0) for n in neighbors(p))
            if grid.get(p):
                new_grid[p] = temp == 1
            else:
                new_grid[p] = 1 <= temp <= 2
    return new_grid


T = open('input').read().split('\n')
grid = {(0, x + 1j * y): c == '#' for y, L in enumerate(T) for x, c in enumerate(L)}

for round in range(200):
    grid = step(grid, round)
print(sum(grid.values()))

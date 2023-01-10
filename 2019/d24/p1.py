def n4(p):
    return [p - 1j, p - 1, p + 1, p + 1j]


def step(grid):
    new_grid = {}
    for p in grid.keys():
        temp = len([1 for n in n4(p) if grid.get(n, False)])
        if grid[p]:
            new_grid[p] = temp == 1
        else:
            new_grid[p] = 1 <= temp <= 2
    return new_grid


def score(grid):
    total = 0
    for x in range(5):
        for y in range(5):
            if grid[x + 1j * y]:
                total += 2**(5 * y + x)
    return total


seen, grid = set(), {}
for y, line in enumerate(open("input").read().split('\n')):
    for x, c in enumerate(line):
        grid[x + 1j * y] = c == '#'

while True:
    temp = score(grid)
    if temp in seen:
        print(temp)
        break
    seen.add(temp)
    grid = step(grid)

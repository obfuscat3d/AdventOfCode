import copy


def north_support(grid):
    y_size = max([p.imag for p in grid])
    return int(sum(y_size - p.imag + 1 for p in grid if grid[p] == "O"))


def move(grid, directions):
    for d in directions:
        for p in sorted(
            [p for p in grid if grid[p] == "O"],
            key=lambda p: -1 * (d.real * p.real + d.imag * p.imag),
        ):
            while p + d in grid and grid[p] == "O" and grid[p + d] == ".":
                grid[p], grid[p + d], p = ".", "O", p + d
    return grid


def part2(grid):
    seen, i = {}, 0
    while True:
        hash = "".join(grid.values())
        if hash in seen and not (1000000000 - seen[hash]) % (i - seen[hash]):
            return north_support(grid)
        seen[hash] = i
        grid, i = move(grid, [-1j, -1, 1j, 1]), i + 1


text = open("input").readlines()
grid = {x + y * 1j: c for y, l in enumerate(text) for x, c in enumerate(l.strip())}
print(north_support(move(copy.deepcopy(grid), [-1j])))
print(part2(copy.deepcopy(grid)))

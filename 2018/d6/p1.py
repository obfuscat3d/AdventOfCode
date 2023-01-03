from collections import deque


def parse(filename):
    points = []
    for l in open(filename).read().split('\n'):
        x, y = l.split(', ')
        points.append(int(x) + 1j * int(y))
    min_x = int(min(p.real for p in points))
    max_x = int(max(p.real for p in points))
    min_y = int(min(p.imag for p in points))
    max_y = int(max(p.imag for p in points))
    return points, min_x, max_x, min_y, max_y


def part1(points, min_x, max_x, min_y, max_y):
    grid, infinite = {}, set()
    queue = deque([(i + 1, p, 0) for i, p in enumerate(points)])
    while queue:
        i, p, d = queue.popleft()
        if p.real in [min_x, max_x] or p.imag in [min_y, max_y]:
            infinite.add(i)
        elif p in grid and i != grid[p][0] and d == grid[p][1]:
            grid[p] = (0, -1)
        elif p not in grid:
            grid[p] = (i, d)
            for n in [p + 1, p - 1, p + 1j, p - 1j]:
                queue.append((i, n, d + 1))
    best = 0
    for q in range(1, len(points) + 1):
        if q not in infinite:
            best = max(len([1 for _, i in grid.items() if i[0] == q]), best)
    print(best)


def md(a, b):
    return abs(a.real - b.real) + abs(a.imag - b.imag)


def part2(points, min_x, max_x, min_y, max_y):
    c = 0
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            if sum([md(x + 1j * y, p) for p in points]) <= 10000:
                c += 1
    print(c)


points, min_x, max_x, min_y, max_y = parse("input")
part1(points, min_x, max_x, min_y, max_y)
part2(points, min_x, max_x, min_y, max_y)

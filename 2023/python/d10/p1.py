def parse(filename):
    graph, grid, start, lines = {}, {}, None, open(filename).readlines()
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            moves = {
                ".": [],
                "|": [(x, y - 1), (x, y + 1)],
                "-": [(x - 1, y), (x + 1, y)],
                "L": [(x, y - 1), (x + 1, y)],
                "J": [(x - 1, y), (x, y - 1)],
                "7": [(x - 1, y), (x, y + 1)],
                "F": [(x + 1, y), (x, y + 1)],
                "S": [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)],
            }
            graph[x, y], grid[x, y] = moves[c], c
            start = (x, y) if c == "S" else start

    return graph, grid, start


def find_path(graph, start):
    path = [start]
    while path[-1] != start or len(path) < 2:
        path.append(
            [
                c
                for c in graph[path[-1]]
                if (path[-1] in graph[c])
                and ((c not in path) or (c == start and len(path) > 2))
            ][0]
        )

    return path


def count_inside(grid, path):
    max_x, max_y = max(x for (x, y) in grid), max(y for (x, y) in grid)
    inside_squares = 0
    for y in range(1 + max_y):
        is_in, fl = False, None
        for x, c in [(x, grid[x, y]) for x in range(1 + max_x)]:
            if (x, y) in path:
                if c == "|" or c == "S":
                    is_in = not is_in
                elif c in ["F", "L"]:
                    fl = c
                elif (fl == "F" and c == "J") or (fl == "L" and c == "7"):
                    is_in = not is_in
            else:
                inside_squares += is_in
    return inside_squares


def count_inside_shoelace(path):
    total = 0
    for a, b in zip(path, path[1:] + [path[0]]):
        total += (a[0] * b[1]) - (a[1] * b[0])
    return (total - len(path) + 3) // 2


graph, grid, start = parse("input")
path = find_path(graph, start)
print(len(path) // 2)
print(count_inside(grid, path))
print(count_inside_shoelace(path))

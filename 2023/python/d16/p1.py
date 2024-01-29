def part1(grid, start=(-1, 1)):
    bq, seen = [start], set()
    while bq:
        p, d = bq.pop()
        if (p, d) in seen:
            continue
        seen.add((p, d))
        if p + d not in grid:
            continue
        if grid[p + d] == "|" and d.real:
            bq.extend([(p + d, -1j), (p + d, 1j)])
        elif grid[p + d] == "-" and d.imag:
            bq.extend([(p + d, -1), (p + d, 1)])
        elif grid[p + d] == "/":
            bq.append((p + d, -d.imag - 1j * d.real))
        elif grid[p + d] == "\\":
            bq.append((p + d, d.imag + 1j * d.real))
        else:
            bq.append((p + d, d))
    return len(set(p for p, _ in seen)) - 1


def part2(grid):
    mx, my, best = max(int(x.real) for x in grid), max(int(p.imag) for p in grid), 0
    for x in range(mx + 1):
        best = max(best, part1(grid, (x - 1j, 1j)))
        best = max(best, part1(grid, (x + 1j * (my + 1), -1j)))
    for y in range(my + 1):
        best = max(best, part1(grid, (-1 + 1j * y, 1)))
        best = max(best, part1(grid, (mx + (1j * my + 1), -1)))
    return best


text = open("input").readlines()
grid = {x + y * 1j: c for y, l in enumerate(text) for x, c in enumerate(l.strip())}
print(part1(grid))
print(part2(grid))

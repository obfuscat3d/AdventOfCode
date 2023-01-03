from collections import deque
import re


def parse(filename):
    text = open(filename).read()
    lines = text.split('\n')
    grid = {}
    for l in lines:
        a, b, c = map(int, re.findall("\d+", l))
        if l[0] == 'x':
            for y in range(b, c + 1):
                grid[a + 1j * y] = 'C'
        else:
            for x in range(b, c + 1):
                grid[x + 1j * a] = 'C'
    return grid


def part_1_and_2(grid):
    min_y = min(int(p.imag) for p in grid.keys())
    max_y = max(int(p.imag) for p in grid.keys())
    queue = deque([500])

    while queue:
        w = queue.pop()
        while grid.get(w + 1j, ' ') not in ['~', 'C'] and w.imag <= max_y:
            grid[w] = '|'
            w += 1j
        if w.imag > max_y:
            continue

        grid[w], left, right = '|', w, w
        while (grid.get(left - 1, ' ') in [' ', '|'] and
               grid.get(left - 1 + 1j, ' ') in ['~', 'C']):
            left -= 1
            grid[left] = '|'

        while (grid.get(right + 1, ' ') in [' ', '|'] and
               grid.get(right + 1 + 1j, ' ') in ['~', 'C']):
            right += 1
            grid[right] = '|'

        if grid.get(left - 1, ' ') in ['~', 'C'] and grid.get(right + 1, ' ') in ['~', 'C']:
            for x in range(int(left.real), int(right.real) + 1):
                grid[x + 1j * w.imag] = '~'
            queue.append(w - 1j)

        if grid.get(right + 1 + 1j, ' ') not in ['~', 'C']:
            queue.append(right + 1)

        if grid.get(left - 1 + 1j, ' ') not in ['~', 'C']:
            queue.append(left - 1)

    print(len([1 for p, v in grid.items() if v in ['|', '~'] and p.imag >= min_y]))
    print(len([1 for p, v in grid.items() if v in ['~'] and p.imag >= min_y]))


part_1_and_2(parse("input"))

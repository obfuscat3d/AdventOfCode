"""
Python. Because fuck parsing this in Clojure.
"""

from collections import deque
import string
from itertools import *


def parse(filename):
    lines = open(filename).read().split('\n')
    grid = {x + 1j * y: c for y, L in enumerate(lines) for x, c in enumerate(L)}
    width, height = len(lines[0]), len(lines)
    return grid, width, height


def n4(p):
    return [p - 1j, p - 1, p + 1, p + 1j]


def is_inner(p, width, height):
    return 4 <= p.imag <= height - 4 and 4 <= p.real <= width - 4


def build_teleports(grid, width, height):
    teleports = {}
    for x, y in product(range(width), range(height)):
        p = x + 1j * y
        if grid[p] in string.ascii_uppercase and any(grid.get(n, None) == '.' for n in n4(p)):
            for d in n4(0):
                if grid[p + d] in string.ascii_uppercase:
                    label = grid[p] + grid[p + d] if d in [1, 1j] else grid[p + d] + grid[p]
                    if label in teleports:
                        teleports[p - d] = teleports[label]
                        teleports[teleports[label]] = p - d
                        del teleports[label]
                    else:
                        teleports[label] = p - d
    return teleports


def part1(grid, teleports):
    seen, queue = set(), deque([(teleports['AA'], 0)])
    while queue:
        p, path_len = queue.popleft()
        if p == teleports['ZZ']:
            print(path_len)
            return
        elif p in teleports and teleports[p] not in seen:
            seen.add(teleports[p])
            queue.append((teleports[p], path_len + 1))
        else:
            for n in [q for q in n4(p) if grid[q] == '.' and q not in seen]:
                seen.add(n)
                queue.append((n, path_len + 1))


def part2(grid, teleports, width, height):
    seen, queue = set(), deque([(teleports['AA'], 0, 0, False)])
    while queue:
        p, level, path_len, just_teleported = queue.popleft()
        if p == teleports['ZZ'] and level == 0:
            print(path_len)
            return
        elif p in teleports and not just_teleported:
            if is_inner(p, width, height) or level > 0:
                new_level = level + 1 if is_inner(p, width, height) else level - 1
                queue.append((teleports[p], new_level, path_len + 1, True))
        else:
            for n in [q for q in n4(p) if grid[q] == '.' and (q, level) not in seen]:
                seen.add((n, level))
                queue.append((n, level, path_len + 1, False))


grid, width, height = parse("input")
teleports = build_teleports(grid, width, height)
part1(grid, teleports)
part2(grid, teleports, width, height)

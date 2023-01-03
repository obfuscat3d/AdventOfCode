import cProfile
from collections import defaultdict, deque
from heapq import *


def parse():
    BLIZ_TYPES = {'<': -1, '>': 1, '^': -1j, 'v': 1j}
    text = open("input").read().strip().split('\n')
    bliz_list = []
    for y, line in enumerate(text):
        for x, char in enumerate(line):
            if char in BLIZ_TYPES:
                bliz_list.append(((x - 1) + 1j * (y - 1), BLIZ_TYPES[char]))
    width, height = len(text[0]) - 2, len(text) - 2
    start, end = -1j, width - 1 + 1j * height
    return bliz_list, width, height, start, end


def move_opts(width, height, all_waypoints, a):
    return {p for p in [a, a - 1, a + 1, a - 1j, a + 1j]
            if p in all_waypoints or (0 <= p.real < width and 0 <= p.imag < height)}


def bliz_iter(bliz_list, width, height):
    return [((a[0].real + a[1].real) % width + 1j * ((a[0].imag + a[1].imag) % height), a[1]) for a in bliz_list]


def md(a, b):
    return abs((a - b).real) + abs((a - b).imag)


def run(init_bliz, width, height, start, init_waypoints):
    bliz_lists, seen, queue, inc = {0: init_bliz}, set(), [], 1
    bliz_sets = {0: {a[0] for a in bliz_lists[0]}}
    heappush(queue, (md(start, init_waypoints[0]), 0, 0, start, init_waypoints))
    while queue:
        _, _, t, p, ws = heappop(queue)

        if p == ws[0]:
            ws = ws[1:]
            queue = []
        if not ws:
            return t

        if not t + 1 in bliz_lists:
            bliz_lists[t + 1] = bliz_iter(bliz_lists[t], width, height)
            bliz_sets[t + 1] = {a[0] for a in bliz_lists[t + 1]}
        for o in move_opts(width, height, init_waypoints, p):
            if not o in bliz_sets[t + 1] and not (t + 1, o, ws) in seen:
                seen.add((t + 1, o, ws))
                inc += 1
                heappush(queue, (t + md(ws[0], o), inc, t + 1, o, ws))


init_bliz, width, height, start, end = parse()
print(run(init_bliz, width, height, start, (end,)))
print(run(init_bliz, width, height, start, (end, start, end)))

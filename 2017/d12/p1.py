from collections import deque
import re


def parse(filename):
    progs = {}
    for l in open(filename).read().split('\n'):
        a, *xs = re.findall("\d+", l)
        progs[a] = xs
    return progs


def calc_group(data, start):
    seen, queue = set(), deque([start])
    while queue:
        cur = queue.popleft()
        if cur in seen:
            continue
        seen.add(cur)
        queue.extend(data[cur])
    return seen


def part1(data):
    print(len(calc_group(data, '0')))


def part2(data):
    groups, unseen = 0, set(data.keys())
    while unseen:
        seen = calc_group(data, unseen.pop())
        unseen, groups = unseen - seen, groups + 1
    print(groups)


data = parse("input")
part1(data)
part2(data)

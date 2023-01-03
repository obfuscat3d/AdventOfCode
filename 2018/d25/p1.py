import re


def parse(filename):
    lines = open(filename).read().split('\n')
    return [tuple(map(int, re.findall("-?\d+", l))) for l in lines]


def md(a, b):
    return sum(map(abs, [i - j for i, j in zip(a, b)]))


def add_point(constellations, p):
    joined, i = None, 0
    while i < len(constellations):
        c = constellations[i]
        for m in c:
            if md(p, m) <= 3 and not joined:
                c.append(p)
                joined = c
                break
            elif md(p, m) <= 3:
                joined += c
                del constellations[i]
                i -= 1
                break
        i += 1
    if not joined:
        constellations.append([p])
    return constellations


def part1(data):
    constellations = []
    for p in data:
        constellations = add_point(constellations, p)
    print(len(constellations))


data = parse("input")
part1(data)

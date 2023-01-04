import re
from collections import defaultdict
from copy import deepcopy


def parse(filename):
    i, particles = 0, []
    for l in open(filename).read().split('\n'):
        particles.append([i] + list(map(int, re.findall("-?\d+", l))))
        i += 1
    return particles


def step(p):
    p[4] += p[7]
    p[5] += p[8]
    p[6] += p[9]
    p[1] += p[4]
    p[2] += p[5]
    p[3] += p[6]


def part1(particles):
    for _ in range(500):  # arbitrary guess
        for p in particles:
            step(p)
    print(sorted(particles, key=lambda x: sum(map(abs, x[1:4])))[0][0])


def part2(particles):
    for _ in range(500):  # arbitrary guess
        positions = defaultdict(int)
        for p in particles:
            step(p)
            positions[tuple(p[1:4])] += 1
        particles = [p for p in particles if positions[tuple(p[1:4])] < 2]

    print(len(particles))


particles = parse('input')
part1(deepcopy(particles))
part2(deepcopy(particles))

import re
from copy import deepcopy
import math


class Monkey:
    def __init__(self, s):
        lines = s.split('\n')
        self.items = list(map(int, re.findall("\d+", lines[1])))
        self.test = int(re.findall("\d+", lines[3])[0])
        self.if_true = int(re.findall("\d+", lines[4])[0])
        self.if_false = int(re.findall("\d+", lines[5])[0])
        self.inspections = 0

        if not re.search("\d", lines[2]):
            self.op = (lambda x: x * x) if '*' in lines[2] else (lambda x: x + x)
        else:
            y = int(re.findall("\d+", lines[2])[0])
            self.op = (lambda x: x * y) if '*' in lines[2] else (lambda x: x + y)

    def turn(self, monkeys, lcm):
        for item in self.items:
            self.inspections += 1
            item = self.op(item) % lcm if lcm else self.op(item) // 3
            monkeys[self.if_false if item % self.test else self.if_true].items.append(item)
        self.items = []


def run_sim(monkeys, rounds, lcm):
    for _ in range(rounds):
        for m in monkeys:
            m.turn(monkeys, lcm)
    return monkeys


def monkey_business(monkeys):
    x = sorted([m.inspections for m in monkeys], reverse=True)
    return x[0] * x[1]


def part1(monkeys):
    print(monkey_business(run_sim(monkeys, 20, 0)))


def part2(monkeys):
    print(monkey_business(run_sim(monkeys, 10_000, math.lcm(*[m.test for m in monkeys]))))


monkeys = [Monkey(s) for s in open('input').read().split('\n\n')]
part1(deepcopy(monkeys))
part2(deepcopy(monkeys))

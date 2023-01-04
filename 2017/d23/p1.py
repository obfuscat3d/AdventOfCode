"""
Part 2 changes the instruction definitions, so check out p2.py for that.
"""

from collections import defaultdict
from dataclasses import dataclass


@dataclass
class State:
    ip: int
    reg: dict
    mul_cnt: int = 0


def parse(filename):
    return [tuple(l.split()) for l in open(filename).read().split('\n')]


def step(instructions, state):
    ins = instructions[state.ip]

    a, b, c = ins
    valB = int(b) if b.lstrip('-').isnumeric() else state.reg[b]
    valC = int(c) if c.lstrip('-').isnumeric() else state.reg[c]
    if a == "set":
        state.reg[b] = valC
    elif a == "sub":
        state.reg[b] -= valC
    elif a == "mul":
        state.reg[b] *= valC
        state.mul_cnt += 1
    elif a == "jnz":
        if valB != 0:
            state.ip += valC - 1
    state.ip += 1
    return state


def part1(instructions):
    state = State(0, defaultdict(int))
    while 0 <= state.ip < len(instructions):
        state = step(instructions, state)
    print(state.mul_cnt)


def part2(instructions):
    """
    Manual inspection of the instructions led to the belief that it's counting
    compisite numbers for a certain interval between two bounds. Code below 
    should generalize to other inputs assuming only the bounds an interval
    change.

    (I doubt the interval changes though, mine is 17 and the year is 2017)
    """
    state = State(0, defaultdict(int))
    state.reg['a'] = 1
    for _ in range(10):
        state = step(instructions, state)

    # laziest prime test for n > 2 ever, still works in a third of a second
    isp = lambda x: x % 2 == 1 and all(x % y for y in range(3, x, 2))
    upper, lower, interval = state.reg['c'], state.reg['b'], -int(instructions[-2][2])
    print(len([1 for i in range(lower, upper + 1, interval) if not isp(i)]))


instructions = parse("input")
part1(instructions)
part2(instructions)

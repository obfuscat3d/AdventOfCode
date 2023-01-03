"""
Part 2 changes the instruction definitions, so check out p2.py for that.
"""

from collections import defaultdict
from dataclasses import dataclass


@dataclass
class State:
    ip: int
    reg: dict
    sounds: list
    rcv_sounds: list


def parse(filename):
    return [tuple(l.split()) for l in open(filename).read().split('\n')]


def step(instructions, state):
    ins = instructions[state.ip]
    if ins[0] == 'snd':
        state.sounds.append(state.reg[ins[1]])
    elif ins[0] == 'rcv':
        if state.reg[ins[1]]:
            state.rcv_sounds.append(state.sounds.pop())
    else:
        a, b, c = ins
        valB = int(b) if b.lstrip('-').isnumeric() else state.reg[b]
        valC = int(c) if c.lstrip('-').isnumeric() else state.reg[c]
        if a == "set":
            state.reg[b] = valC
        elif a == "add":
            state.reg[b] += valC
        elif a == "mul":
            state.reg[b] *= valC
        elif a == "mod":
            state.reg[b] %= valC
        elif a == "jgz":
            if valB > 0:
                state.ip += valC - 1
    state.ip += 1
    return state


def part1(instructions):
    state = State(0, defaultdict(int), [], [])
    while not state.rcv_sounds:
        state = step(instructions, state)
    print(state.rcv_sounds[0])


data = parse("input")
part1(data)

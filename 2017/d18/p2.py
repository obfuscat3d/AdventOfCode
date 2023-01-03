"""
Part 1 changes the instruction definitions, so check out p1.py for that.
"""


from collections import defaultdict, deque
from dataclasses import dataclass


@dataclass
class State:
    reg: dict
    buffer: deque
    dest: deque
    ip: int = 0
    sent_count: int = 0
    blocked: bool = False


def parse(filename):
    text = open(filename).read()
    lines = text.split('\n')
    return [tuple(l.split()) for l in lines]


def step(instructions, state):
    ins = instructions[state.ip]
    if ins[0] == 'snd':
        state.sent_count += 1
        state.dest.append(state.reg[ins[1]])
    elif ins[0] == 'rcv':
        if state.buffer:
            state.blocked = False
            state.reg[ins[1]] = state.buffer.popleft()
        else:
            state.blocked = True
            return state  # note the early return to preserve state.ip
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


def part2(instructions):
    s0_buffer, s1_buffer = deque(), deque()
    state0 = State(defaultdict(int), s0_buffer, s1_buffer)
    state1 = State(defaultdict(int), s1_buffer, s0_buffer)
    state1.reg['p'] = 1
    while not (state0.blocked and state1.blocked):
        state0 = step(instructions, state0)
        state1 = step(instructions, state1)
    print(state1.sent_count)


data = parse("input")
part2(data)

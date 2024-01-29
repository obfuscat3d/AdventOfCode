from collections import defaultdict, namedtuple
from math import lcm

LOW, HIGH = False, True
Pulse = namedtuple("Pulse", ["sender", "recipient", "is_high"])


def parse_config(filename):
    flip_flops = set()
    conjunctions = set()
    connections_out = defaultdict(list)
    connections_in = defaultdict(list)
    for l in open(filename).readlines():
        label, ends = l.split(" -> ")
        connections_out[label[1:]] = [e.strip() for e in ends.split(",")]
        for e in connections_out[label[1:]]:
            connections_in[e].append(label[1:])
        if label[0] == "%":
            flip_flops.add(label[1:])
        elif label[0] == "&":
            conjunctions.add(label[1:])

    return (flip_flops, conjunctions, connections_out, connections_in)


def make_state(config):
    flip_flops, conjunctions, _, connections_in = config
    flip_flop_state = {f: LOW for f in flip_flops}
    conjunction_state = {}
    for c in conjunctions:
        conjunction_state[c] = {inp: LOW for inp in connections_in[c]}
    return (flip_flop_state, conjunction_state)


def press_button(config, state):
    flip_flops, conjunctions, connections_out, _ = config
    q, pulses = [Pulse("button", "roadcaster", LOW)], []  # this is not a typo
    while q:
        p = q.pop(0)
        pulses.append(p)
        if p.recipient in flip_flops:
            if not p.is_high:
                to_send = state[0][p.recipient] = not state[0][p.recipient]
                for out in connections_out[p.recipient]:
                    q.append(Pulse(p.recipient, out, to_send))
        elif p.recipient in conjunctions:
            state[1][p.recipient][p.sender] = p.is_high
            to_send = not all(state[1][p.recipient].values())
            for out in connections_out[p.recipient]:
                q.append(Pulse(p.recipient, out, to_send))
        else:  # broadcaster
            for out in connections_out[p.recipient]:
                q.append(Pulse(p.recipient, out, LOW))

    return state, pulses


def part1(config):
    low_count, high_count = 0, 0
    state = make_state(config)
    for _ in range(1000):
        state, pulses = press_button(config, state)
        low_count += sum(1 for p in pulses if not p.is_high)
        high_count += sum(1 for p in pulses if p.is_high)
    print(low_count * high_count)


def part2(config):
    _, _, _, connections_in = config
    state, i = make_state(config), 0
    to_watch = connections_in[connections_in["rx"][0]]  # NAND gate pointing to rx
    first_high_pulse = {x: 0 for x in to_watch}
    while not all(first_high_pulse.values()):
        i += 1
        state, pulses = press_button(config, state)
        for p in pulses:
            if p.is_high and p.sender in to_watch and not first_high_pulse[p.sender]:
                first_high_pulse[p[0]] = i
    print(lcm(*first_high_pulse.values()))


config = parse_config("input")
part1(config)
part2(config)

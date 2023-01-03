from collections import Counter
import re


def parse(filename):
    nodes = {}
    for l in open(filename).read().split('\n'):
        name, weight, *x = re.findall("\w+", l)
        nodes[name] = (name, int(weight), x)
    return nodes


def recursive_weight(nodes, node):
    x = node[1]
    for c in node[2]:
        x += recursive_weight(nodes, nodes[c])
    return x


def unbal(nodes, node, diff):
    if not node[2]:
        return node[0] + diff
    weights = {c: recursive_weight(nodes, nodes[c]) for c in node[2]}
    counter = Counter(weights.values())
    if len(counter) == 1:
        return node[1] + diff
    for k, v in counter.items():
        if v == 1:
            bad_v = k
        else:
            good_v = k
    baddie = [k for k, v in weights.items() if v == bad_v][0]
    return unbal(nodes, nodes[baddie], good_v - bad_v)


def part1(nodes):
    print((set(nodes.keys()) - {c for n in nodes.values() for c in n[2]}).pop())


def part2(nodes):
    root = (set(nodes.keys()) - {c for n in nodes.values() for c in n[2]}).pop()
    print(unbal(nodes, nodes[root], 0))


nodes = parse("input")
part1(nodes)
part2(nodes)

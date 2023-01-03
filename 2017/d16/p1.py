from collections import deque
import re


def dance(order, ops):
    for op in ops.split(','):
        if op[0] == 's':
            order.rotate(int(op[1:]))
        elif op[0] == 'p':
            a, b = order.index(op[1]), order.index(op[3])
            order[a], order[b] = op[3], op[1]
        elif op[0] == 'x':
            a, b = map(int, re.findall("\d+", op))
            order[a], order[b] = order[b], order[a]
    return order


def part1(ops):
    print(''.join(dance(deque(list("abcdefghijklmnop")), ops)))


def part2(ops):
    order, seen, i = deque(list("abcdefghijklmnop")), {}, 0
    while True:
        order = dance(order, ops)
        i, s = i + 1, ''.join(order)
        if s in seen and (1_000_000_000 - i) % (i - seen[s]) == 0:
            print(s)
            break
        seen[s] = i


part1(open("input").read())
part2(open("input").read())

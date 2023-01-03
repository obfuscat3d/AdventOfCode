import functools


def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return 0 if a == b else (-1 if a < b else 1)
    elif isinstance(a, int):
        return compare([a], b)
    elif isinstance(b, int):
        return compare(a, [b])
    elif a and b:
        q = compare(a[0], b[0])
        return q if q else compare(a[1:], b[1:])
    return 1 if a else (-1 if b else 0)


pairs, packets = [], [[[2]], [[6]]]
for p in open('input').read().split('\n\n'):
    a, b = map(eval, p.split('\n'))
    pairs.append((a, b))
    packets += [a, b]

print(sum(i + 1 for i, x in enumerate(pairs) if compare(x[0], x[1]) == -1))

packets_sorted = sorted(packets, key=functools.cmp_to_key(compare))
print((1 + packets_sorted.index([[2]])) * (1 + packets_sorted.index([[6]])))

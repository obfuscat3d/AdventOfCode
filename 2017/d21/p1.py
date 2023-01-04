import numpy as np


def s2np(s):
    size = int(np.sqrt(len(s)))
    return np.resize([c == '#' for c in s], (size, size)).astype(bool)


def parse(filename):
    lines = open(filename).read().split('\n')
    rules = {}
    for l in lines:
        pattern, result = l.split(" => ")
        pattern, result = s2np(pattern.replace('/', '')), s2np(result.replace('/', ''))
        pattern2 = np.fliplr(pattern)
        for _ in range(4):
            rules[pattern.tobytes()] = result
            rules[pattern2.tobytes()] = result
            pattern, pattern2 = np.rot90(pattern), np.rot90(pattern2)

    return rules


def step(rules, A):
    size = A.shape[0]
    us = 3 if size % 2 else 2
    result = np.zeros((size * (us + 1) // us, size * (us + 1) // us), dtype=bool)
    for x in range(size // us):
        for y in range(size // us):
            temp = A[us * x: us * x + us, us * y: us * y + us]
            temp2 = rules[temp.tobytes()]
            result[(us + 1) * x: (us + 1) * x + (us + 1), (us + 1) * y: (us + 1) * y + (us + 1)] = temp2
    return result


def run(rules, n):
    A = s2np(".#...####")
    for i in range(n):
        A = step(rules, A)
    print(np.count_nonzero(A))


rules = parse("input")
run(rules, 5)
run(rules, 18)

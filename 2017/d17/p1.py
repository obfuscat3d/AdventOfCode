from collections import deque
INPUT = 370


def part1():
    q = deque()
    for i in range(2018):
        q.rotate(-INPUT)
        q.append(i)
    print(q[0])


def part2():
    q = deque()
    for i in range(50_000_001):
        q.rotate(-INPUT)
        q.append(i)
    print(q[q.index(0) + 1])


def part2_optimized():
    p, l, ans = 0, 1, None
    for i in range(1, 50_000_001):
        p = (p + INPUT) % l + 1
        ans = i if p == 1 else ans
        l += 1
    print(ans)


part1()
part2_optimized()

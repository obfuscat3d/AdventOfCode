DIGITS = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
STIGID = {0: '0', 1: '1', 2: '2', -1: '-', -2: '='}


def snafu2int(line):
    return sum([5**i * DIGITS[c] for i, c in enumerate(line[::-1])])


def int2snafu(n):
    s = STIGID[((n + 2) % 5) - 2]
    while n := (n - ((n + 2) % 5) + 2) // 5:
        s += STIGID[((n + 2) % 5) - 2]
    return s[::-1]


text = open("input").read().split('\n')
print(int2snafu(sum(snafu2int(line) for line in text)))

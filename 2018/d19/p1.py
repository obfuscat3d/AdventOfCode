import re


def mk_op(op, immA, immB):
    def o(R, a, b, c):
        R = R.copy()
        R[c] = op(a if immA else R[a], b if immB else R[b])
        return R
    return o


OPS = {
    'addr': mk_op(lambda x, y: x + y, False, False),
    'addi': mk_op(lambda x, y: x + y, False, True),
    'mulr': mk_op(lambda x, y: x * y, False, False),
    'muli': mk_op(lambda x, y: x * y, False, True),
    'banr': mk_op(lambda x, y: x & y, False, False),
    'bani': mk_op(lambda x, y: x & y, False, True),
    'borr': mk_op(lambda x, y: x | y, False, False),
    'bori': mk_op(lambda x, y: x | y, False, True),
    'setr': mk_op(lambda x, y: x, False, True),
    'seti': mk_op(lambda x, y: x, True, True),
    'gtir': mk_op(lambda x, y: x > y, True, False),
    'gtri': mk_op(lambda x, y: x > y, False, True),
    'gtrr': mk_op(lambda x, y: x > y, False, False),
    'eqir': mk_op(lambda x, y: x == y, True, False),
    'eqri': mk_op(lambda x, y: x == y, False, True),
    'eqrr': mk_op(lambda x, y: x == y, False, False)
}


def parse(filename):
    text = open(filename).read().split('\n')
    ip = int(text.pop(0)[4])
    ins = []
    for line in text:
        a, b, c = re.findall("\d+", line)
        ins.append((line[0:4], int(a), int(b), int(c)))
    return ip, ins


def part1(ip, ins):
    R = [0] * 6
    while 0 <= R[ip] < len(ins):
        op, a, b, c = ins[R[ip]]
        R = OPS[op](R, a, b, c)
        R[ip] += 1
    print(R[0])


def part2(ip, ins):
    # Figured out the pattern manually
    R, i = [1, 0, 0, 0, 0, 0], 200
    while i and 0 <= R[ip] < len(ins):
        op, a, b, c = ins[R[ip]]
        R = OPS[op](R, a, b, c)
        R[ip], i = R[ip] + 1, i - 1
    dividend = R[2]
    print(sum([i for i in range(1, dividend + 1) if dividend % i == 0]))


ip, ins = parse("input")
part1(ip, ins)
part2(ip, ins)

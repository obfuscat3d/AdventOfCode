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
    R = [0, 0, 0, 0, 0, 0]
    while 0 <= R[ip] < len(ins):
        op, a, b, c = ins[R[ip]]
        if R[ip] == 28:
            print(R[4])
            return
        R = OPS[op](R, a, b, c)
        R[ip] = R[ip] + 1

    # print(16128384)


def part2(ip, ins):
    R, seen, last = [0, 0, 0, 0, 0, 0], set(), 0
    while 0 <= R[ip] < len(ins):
        op, a, b, c = ins[R[ip]]
        if R[ip] == 28:
            if R[4] in seen:
                print(last)
                return
            else:
                last = R[4]
                seen.add(R[4])
        R = OPS[op](R, a, b, c)
        R[ip] = R[ip] + 1


ip, ins = parse("input")
part1(ip, ins)
part2(ip, ins)

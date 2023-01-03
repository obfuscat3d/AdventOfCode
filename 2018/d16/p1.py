import re


def mk_op(op, immA, immB):
    def o(R, a, b, c):
        R = R.copy()
        R[c] = op(a if immA else R[a], b if immB else R[b])
        return R
    return o


addr = mk_op(lambda x, y: x + y, False, False)
addi = mk_op(lambda x, y: x + y, False, True)
mulr = mk_op(lambda x, y: x * y, False, False)
muli = mk_op(lambda x, y: x * y, False, True)
banr = mk_op(lambda x, y: x & y, False, False)
bani = mk_op(lambda x, y: x & y, False, True)
borr = mk_op(lambda x, y: x | y, False, False)
bori = mk_op(lambda x, y: x | y, False, True)
setr = mk_op(lambda x, y: x, False, False)
seti = mk_op(lambda x, y: x, True, False)
gtir = mk_op(lambda x, y: x > y, True, False)
gtri = mk_op(lambda x, y: x > y, False, True)
gtrr = mk_op(lambda x, y: x > y, False, False)
eqir = mk_op(lambda x, y: x == y, True, False)
eqri = mk_op(lambda x, y: x == y, False, True)
eqrr = mk_op(lambda x, y: x == y, False, False)
OPS = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtri, gtir, gtrr, eqri, eqir, eqrr]


def parse(filename):
    example_text, instruction_text = open(filename).read().split("\n\n\n\n")
    examples = []
    for e in example_text.split("\n\n"):
        lines = e.split("\n")
        before = list(map(int, re.findall("\d+", lines[0])))
        ins = list(map(int, re.findall("\d+", lines[1])))
        after = list(map(int, re.findall("\d+", lines[2])))
        examples.append((before, ins, after))

    instructions = []
    for i in instruction_text.split("\n"):
        instructions.append(list(map(int, re.findall("\d+", i))))

    return examples, instructions


def part1(examples):
    match_3 = 0
    for e in examples:
        tr = 0
        for op in OPS:
            if e[2] == op(e[0], e[1][1], e[1][2], e[1][3]):
                tr += 1
        if tr >= 3:
            match_3 += 1
    print(match_3)


def solve_op_codes(examples):
    possible = [OPS.copy() for _ in range(16)]
    for e in examples:
        op_code = e[1][0]
        for op in OPS:
            if e[2] != op(e[0], e[1][1], e[1][2], e[1][3]):
                if op in possible[op_code]:
                    possible[op_code].remove(op)
    while not all(len(possible[i]) == 1 for i in range(16)):
        for op_code in range(16):
            if len(possible[op_code]) == 1:
                for op_code2 in range(16):
                    if op_code2 != op_code and possible[op_code][0] in possible[op_code2]:
                        possible[op_code2].remove(possible[op_code][0])

    return {i: possible[i][0] for i in range(16)}


def part2(examples, instructions):
    op_map = solve_op_codes(examples)
    R = [0, 0, 0, 0]
    for i in instructions:
        R = op_map[i[0]](R, i[1], i[2], i[3])
    print(R[0])


examples, instructions = parse("input")
part1(examples)
part2(examples, instructions)

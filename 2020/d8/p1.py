import copy

FILE = '2020/d8/input'


def run(program):
    seen, acc, pc = [], 0, 0
    while pc not in seen and pc < len(program):
        seen.append(pc)
        if program[pc][0] == 'acc':
            acc += program[pc][1]
        elif program[pc][0] == 'jmp':
            pc += program[pc][1] - 1
        pc += 1
    return (pc >= len(program), acc)


with open(FILE) as input:
    program = [[r[:3], int(r[4:])] for r in input.read().splitlines()]

# part 1
print(run(program)[1])

# part 2
for x in range(len(program)):
    temp_pgm = copy.deepcopy(program)
    if temp_pgm[x][0] == 'jmp':
        temp_pgm[x][0] = 'nop'
    elif temp_pgm[x][0] == 'nop':
        temp_pgm[x][0] = 'jmp'
    output = run(temp_pgm)
    if output[0]:
        print(output[0], output[1])

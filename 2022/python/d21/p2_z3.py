from z3 import *


def create_vars(input):
    vars = {}
    for l in input.split('\n'):
        vars[l[:4]] = Real(l[:4])
    return vars


def add_eq(s, vars, f):
    if len(f) == 2:
        s.add(vars[f[0][:4]] == int(f[1]))
    elif f[2] == '+':
        s.add(vars[f[0][:4]] == vars[f[1]] + vars[f[3]])
    elif f[2] == '*':
        s.add(vars[f[0][:4]] == vars[f[1]] * vars[f[3]])
    elif f[2] == '/':
        s.add(vars[f[0][:4]] == vars[f[1]] / vars[f[3]])
        s.add(vars[f[3]] != 0)
    elif f[2] == '-':
        s.add(vars[f[0][:4]] == vars[f[1]] - vars[f[3]])


def part1(input):
    s, vars = Solver(), create_vars(input)
    for l in input.split('\n'):
        add_eq(s, vars, l.split(' '))
    s.check()
    print(s.model().eval(vars['root']))


def part2(input):
    s, vars = Solver(), create_vars(input)
    for l in input.split('\n'):
        f = l.split(' ')
        if f[0][:4] == 'humn':
            continue
        elif f[0][:4] == 'root':
            s.add(vars[f[1]] == vars[f[3]])
        else:
            add_eq(s, vars, l.split(' '))

    s.check()
    print(s.model().eval(vars['humn']))


input = open('input2').read()
part1(input)
part2(input)

import re


def solve(problem):
    parens = re.findall("\([^\(\)]+\)", problem)
    while parens:
        problem = problem.replace(parens[0], str(solve(parens[0][1:-1])), 1)
        parens = re.findall("\([^\(\)]+\)", problem)

    add = re.findall("\d+ \+ \d+", problem)
    while add:
        problem = problem.replace(add[0], str(eval(add[0])), 1)
        add = re.findall("\d+ \+ \d+", problem)

    return eval(problem)


with open('2020/d18/input') as input:
    print(sum([solve(problem) for problem in input.read().splitlines()]))

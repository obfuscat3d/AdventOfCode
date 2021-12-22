import re


def solve(problem):
    parens = re.findall("\([^\(\)]+\)", problem)
    while parens:
        problem = problem.replace(parens[0], str(solve(parens[0][1:-1])))
        parens = re.findall("\([^\(\)]+\)", problem)

    numbers = [int(n) for n in re.split("[^\d]+", problem)]
    operators = [op for op in re.split("[^\+\*]+", problem) if op]
    while operators:
        if operators.pop(0) == '+':
            numbers.insert(0, numbers.pop(0) + numbers.pop(0))
        else:
            numbers.insert(0, numbers.pop(0) * numbers.pop(0))
    return numbers.pop()


with open('2020/d18/input') as input:
    print(sum([solve(problem) for problem in input.read().splitlines()]))

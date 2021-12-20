import re


def check(rule, x):
    numbers = rule[1]
    return (numbers[0] <= x <= numbers[1] or
            numbers[2] <= x <= numbers[3])


def parse_rules(text):
    rules = []
    for x in text.splitlines():
        [name, rest] = x.split(': ')
        numbers = [int(n) for n in re.split('[^\d]+', rest)]
        rules.append((name, numbers))
    return rules


def parse_nearby(text):
    text = text.split('\n')[1:]
    return [[int(n) for n in nearby.split(',')] for nearby in text]


with open('2020/d16/input') as input:
    [rules_text, my_ticket, nearby_text] = input.read().split('\n\n')

rules = parse_rules(rules_text)
nearby = parse_nearby(nearby_text)

bad = []
for p in nearby:
    for n in p:
        good = False
        for r in rules:
            if check(r, n):
                good = True
        if not good:
            bad.append(n)
print(sum(bad))

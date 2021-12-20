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


def valid(rules, ticket):
    for value in ticket:
        if not [1 for r in rules if check(r, value)]:
            return False
    return True


def possible_rule_indices(rule, nearby):
    ret = []
    for i in range(len(nearby[0])):
        values = [ticket[i] for ticket in nearby]
        if not [1 for value in values if not check(rule, value)]:
            ret.append(i)
    return ret


def match_rules(rules, nearby):
    matches = {}
    possible_matches = [(r[0], possible_rule_indices(r, nearby))
                        for r in rules]
    while possible_matches:
        done = [match for match in possible_matches if len(match[1]) == 1]
        for d in done:
            matches[d[0]] = d[1][0]
            for m in possible_matches:
                m[1].remove(matches[d[0]])
        possible_matches = [m for m in possible_matches if m[1]]
    return matches


with open('2020/d16/input') as input:
    [rules_text, my_ticket, nearby_text] = input.read().split('\n\n')

rules = parse_rules(rules_text)
nearby = [ticket for ticket in parse_nearby(
    nearby_text) if valid(rules, ticket)]
my_ticket = [int(x) for x in my_ticket.split('\n')[1].split(',')]

rule_matches = match_rules(rules, nearby)
departure_product = 1
for match in rule_matches:
    if match.startswith('departure'):
        departure_product *= my_ticket[rule_matches[match]]
print(departure_product)

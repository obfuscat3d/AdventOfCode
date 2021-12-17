FILE = '2020/d7/input'


def parse_rule(rule):
    r = rule.split(' ')
    return (r[0]+' '+r[1],
            ({r[x + 1]+' '+r[x + 2]: int(r[x])
              for x in range(4, len(r), 4)} if len(r) > 7 else {}))


def is_bag_in(rules, bag, target):
    for x in (rules[bag]):
        if x == target or is_bag_in(rules, x, target):
            return True
    return False


def count_children(rules, bag):
    return sum([(1 + count_children(rules, x))*rules[bag][x] for x in rules[bag]])


with open(FILE) as input:
    rules = {parse_rule(r)[0]: parse_rule(r)[1]
             for r in input.read().splitlines()}

count = 0
for bag in rules:
    if is_bag_in(rules, bag, 'shiny gold'):
        count += 1
print(count)

print(count_children(rules, 'shiny gold'))

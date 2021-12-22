def check(rules, seq, s, depth=0):
    # if s and seq are empty, it's a match. If only one is empty, it's not
    if not s or not seq:
        return not s and not seq

    # Need a depth to break for recusive rules.
    if depth > 500:
        return False

    # Handle atomic token
    if not isinstance(rules[seq[0]], list):
        if s[0] == rules[seq[0]][1]:
            return check(rules, seq[1:], s[1:], depth+1)
        else:
            return False

    # Check if we replace this rule with its children
    return any([check(rules, r + seq[1:], s, depth+1)
                for r in rules[seq[0]]])


def parse_rules(rules_text):
    rules = {}
    for rule in rules_text.split('\n'):
        rule_id, content = rule.split(': ')
        if '"' in content:
            rules[rule_id] = content
        else:
            rules[rule_id] = [rs.split(' ') for rs in content.split(' | ')]
    return rules


with open('2020/d19/input3') as input:
    rules_text, tests = input.read().split('\n\n')

rules = parse_rules(rules_text)
print(len([1 for test in tests.split('\n') if check(rules, ['0'], test, 0)]))

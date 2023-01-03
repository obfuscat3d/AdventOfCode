import re

monkeys = {l[:4]: '(' + l[6:] + ')' for l in open('input').read().split('\n')}
s = "root"
while blah := re.findall("[a-z]{4}", s):
    s = s.replace(blah[0], monkeys[blah[0]])
print(eval(s))

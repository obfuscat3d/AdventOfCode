import re

text = open("input").read().split('\n')
pairs = [[int(x) for x in re.split('-|,', pair)] for pair in text]
pair_sets = [(set(range(x[0], x[1] + 1)), set(range(x[2], x[3] + 1))) for x in pairs]
print(sum([eps[0] & eps[1] in eps for eps in pair_sets]))
print(sum([bool(eps[0] & eps[1]) for eps in pair_sets]))

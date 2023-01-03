import re

elf_pairs_text = open("input").read().split('\n')

elf_pairs = [[int(x) for x in re.split('-|,', elf_pair)]
             for elf_pair in elf_pairs_text]

elf_pairs_sets = [(set(range(x[0], x[1]+1)), set(range(x[2], x[3]+1)))
                  for x in elf_pairs]

print(sum([eps[0] & eps[1] in eps for eps in elf_pairs_sets]))
print(sum([bool(eps[0] & eps[1]) for eps in elf_pairs_sets]))

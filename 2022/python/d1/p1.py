import sys

elfs = [sum([int(i) for i in elf.split('\n')]) for elf in open("input").read().split('\n\n')]
print(max(elfs))
print(sum(sorted(elfs, reverse=True)[:3]))

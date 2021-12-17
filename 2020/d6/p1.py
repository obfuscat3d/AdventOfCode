import string

FILE = '2020/d6/input'

# part 1
with open(FILE) as input:
    counts = [len(set(group.replace('\n', '')))
              for group in input.read().split('\n\n')]
print(sum(counts))

# part 2
with open(FILE) as input:
    counts = [
        len([s for s in string.ascii_lowercase
             if len(group.split('\n')) == len([1 for p in group.split('\n') if s in p])])
        for group in input.read().split('\n\n')]
print(sum(counts))

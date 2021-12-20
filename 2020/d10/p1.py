import functools

FILE = '2020/d10/input2'

with open(FILE) as input:
    numbers = [int(i) for i in input.read().splitlines()]

# Part 1, must use all adapters
numbers += [0, max(numbers)+3]
numbers.sort()
buckets = [0]*4
for x in range(len(numbers)-1):
    buckets[numbers[x+1]-numbers[x]] += 1
print(buckets[3]*buckets[1])


# Part 2, count total possible paths
# Memoize, could use DP as well to the same effect
@functools.cache
def count_paths(start=0):
    if start == max(numbers):
        return 1
    return sum([count_paths(i)
                for i in [j for j in numbers if start < j <= start+3]])


print(count_paths(0))

import itertools

FILE = '2020/d9/input'
PREAMBLE = 25


def first_baddie(numbers):
    for x in range(PREAMBLE, len(numbers)):
        if not [1
                for c in itertools.combinations(numbers[x-PREAMBLE:x], 2)
                if sum(c) == numbers[x]]:
            return numbers[x]


def contiguous_sum_to(numbers, x):
    lo, hi = 0, 1
    s = sum(numbers[lo:hi])
    while s != x:
        [lo, hi] = [lo, hi+1] if s < x else [lo+1, hi]
        s = sum(numbers[lo:hi])
    return min(numbers[lo:hi]) + max(numbers[lo:hi])


with open(FILE) as input:
    numbers = [int(i) for i in input.read().splitlines()]


baddie = first_baddie(numbers)
print(baddie)

print(contiguous_sum_to(numbers, baddie))

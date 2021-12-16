import itertools

FILE = '2020/d1/input'

# These are pretty inefficient implementations. In practice, part1 is doable in O(n) time
# and part 2 in O(n log n) time, but here we're just going for O(n^2) and O(n^3) because
# it doesn't matter with small inputs.

def part1(nums):
  print([a*b for (a, b) in itertools.combinations(nums, 2) if a+b == 2020])

def part2(nums):
  print([a*b*c for (a, b, c) in itertools.combinations(nums, 3) if a+b+c == 2020])

if __name__ == '__main__':
  with open(FILE) as input:
    nums = [int(line) for line in input.read().splitlines()]

  part1(nums)
  part2(nums)

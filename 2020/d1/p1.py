import numpy as np

# Print if two numbers sum to 2020
def part1(nums):
  # Load them in a hashtable and then check linearly ends up O(N) overall
  ht = {i:True for i in nums}
  for x in nums:
    if 2020 - x in ht:
      print(x*(2020-x))

# Print if three numbers sum to 2020
def part2(nums):
  # New tactic, now we sort then go linearly. So O(n log n) overall
  nums.sort()
  for i in nums:
    l,h = 0,len(nums)-1
    while l < h and nums[l]+nums[h]+i != 2020:
      if nums[l]+nums[h]+i < 2020:
        l += 1
      else:
        h -= 1
    if nums[l]+nums[h]+i == 2020:
      print(nums[l], nums[h], i, nums[l]*nums[h]*i)

if __name__ == '__main__':
  with open('input') as input:
    nums = np.array([int(line) for line in input.read().splitlines()])

  part1(nums)
  part2(nums)

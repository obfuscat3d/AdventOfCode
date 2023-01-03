def mix(orig, nums):
    for n in orig:
        old_idx = nums.index(n)
        new_idx = (old_idx + n[1]) % (len(nums) - 1)
        del nums[old_idx]
        nums.insert(new_idx, n)


def print_soln(nums):
    s = 0
    while nums[s][1] != 0:
        s += 1
    print(sum(nums[(s + q) % len(nums)][1] for q in [1000, 2000, 3000]))


def part1(orig):
    nums = orig.copy()
    mix(orig, nums)
    print_soln(nums)


def part2(orig):
    orig = [(a, b * 811589153) for a, b in orig]
    nums = orig.copy()
    for _ in range(10):
        mix(orig, nums)
    print_soln(nums)


orig = list(enumerate(map(int, open("input").read().split('\n'))))
part1(orig)
part2(orig)

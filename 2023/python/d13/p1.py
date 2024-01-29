from pprint import pprint


def parse(fn):
    return [l.split("\n") for l in open(fn).read().split("\n\n")]


def rot90(arr):
    return ["".join(i[::-1]) for i in zip(*arr)]


def horizontal_reflection_diff_count(a):
    temp, diff_count = len(a) // 2, 0
    for i, j in zip(a[:temp], a[: temp - 1 : -1]):
        diff_count += sum(1 for j, k in zip(i, j) if j != k)
    return diff_count


def score_matrix(mat, needed_diff_count):
    for c in range(2, len(mat), 2):
        if horizontal_reflection_diff_count(mat[:c]) == needed_diff_count:
            return 100 * c // 2
    mat = rot90(mat)
    for c in range(2, len(mat), 2):
        if horizontal_reflection_diff_count(mat[:c]) == needed_diff_count:
            return c // 2
    mat = rot90(mat)
    for c in range(2, len(mat), 2):
        if horizontal_reflection_diff_count(mat[:c]) == needed_diff_count:
            return 100 * (len(mat) - c // 2)
    mat = rot90(mat)
    for c in range(2, len(mat), 2):
        if horizontal_reflection_diff_count(mat[:c]) == needed_diff_count:
            return len(mat) - c // 2
    return 0


matricies = parse("input")
print(sum(score_matrix(m, 0) for m in matricies))
print(sum(score_matrix(m, 1) for m in matricies))

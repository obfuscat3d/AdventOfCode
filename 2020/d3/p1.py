import numpy as np

FILE = '2020/d3/input'

def trees_for_slope(grid, dx, dy):
  x,y,trees = 0,0,0
  while x < len(grid):
    trees += grid[x][y % len(grid[x])]
  x += dx
  y += dy
  return trees

with open(FILE) as input:
  grid = [[x == '#' for x in line] for line in input.read().splitlines()]

# Part 1
print(trees_for_slope(grid, 1, 3))

# Part 2
print(np.prod([trees_for_slope(grid, x,y) for (x,y) in [(1,1), (1,3), (1,5), (1,7), (2,1)]]))



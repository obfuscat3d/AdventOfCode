// https://adventofcode.com/day/9

const _ = require('underscore');
const fs = require('fs');

const FILE = 'd9/input';

const raw_data = fs.readFileSync(FILE, 'utf8');
grid = raw_data.split('\n').map((row) => row.split('').map(Number));

// Get neighbors on a 2D grid.
const neighbors = (grid, x, y, diagonal = false) =>
  _.flatten([-1, 0, 1].map(a => [-1, 0, 1].map(b => [x + a, y + b])), 1) // get an array of coords
    .filter(([i, j]) => (
      i >= 0 && j >= 0 && i < grid.length && j < grid.length && // filter so they're valid coords
      (i != x || j != y) && // exclude self
      (diagonal || i == x || y == j))); // optionally exclude diagonal

const xy = (coordArr) => (coordArr[0] << 16) + coordArr[1];
const yx = (coord) => [coord >> 16, coord & ((1 << 16) - 1)];

const isRisk = (grid, x, y) =>
  0 == neighbors(grid, x, y).filter(xy => grid[xy[0]][xy[1]] <= grid[x][y]).length;

function basinSize(grid, x, y) {
  size = 0;
  visited = [];
  stack = [xy([x, y])];
  while (current = stack.pop()) {
    visited.push(current);
    [i, j] = yx(current);
    size++;
    m = neighbors(grid, i, j).filter(([a, b]) => (
      (grid[a][b] != 9) && !_.contains(visited, xy([a, b])) && !_.contains(stack, xy([a, b]))));

    stack = stack.concat(m.map(p => xy(p)));
  }
  return size;
}

basins = []
_.each(_.range(grid.length), x => (
  _.each(_.range(grid[0].length), y => {
    if (isRisk(grid, x, y)) basins.push(basinSize(grid, x, y));
  })));

basins.sort((a, b) => (a - b));
console.log(basins.pop() * basins.pop() * basins.pop());
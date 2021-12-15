// https://adventofcode.com/2021/day/9

const _ = require('underscore');
const fs = require('fs');
const µ = require('../../utils');

const FILE = '2021/d9/input';

const raw_data = fs.readFileSync(FILE, 'utf8');
grid = raw_data.split('\n').map((row) => row.split('').map(Number));

const isRisk = (grid, x, y) =>
  0 == µ.neighbors(grid, x, y).filter(xy => grid[xy[0]][xy[1]] <= grid[x][y]).length;

function basinSize(grid, x, y) {
  size = 0;
  visited = [];
  stack = [µ.xy([x, y])];
  while (current = stack.pop()) {
    visited.push(current);
    [i, j] = µ.yx(current);
    size++;
    m = µ.neighbors(grid, i, j).filter(([a, b]) => (
      (grid[a][b] != 9) && !_.contains(visited, µ.xy([a, b])) && !_.contains(stack, µ.xy([a, b]))));

    stack = stack.concat(m.map(p => µ.xy(p)));
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
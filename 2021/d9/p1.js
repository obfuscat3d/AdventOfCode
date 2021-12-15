// https://adventofcode.com/2021/day/9

const _ = require('underscore');
const fs = require('fs');
const µ = require('../../utils');

const FILE = '2021/d9/input';

const raw_data = fs.readFileSync(FILE, 'utf8');
grid = raw_data.split('\n').map((row) => row.split('').map(Number));

// See if any neighbors have a lower risk score than or equal risk score than me,
// if not then I'm at risk.
const isRisk = (grid, x, y) =>
  0 == µ.neighbors(grid, x, y).filter(([i,j]) => grid[i][j] <= grid[x][y]).length;

riskSum = 0;
_.each(_.range(grid.length), x => (
  _.each(_.range(grid[0].length), y => (
      riskSum += isRisk(grid, x, y) ? grid[x][y] + 1 : 0))));

console.log(riskSum);
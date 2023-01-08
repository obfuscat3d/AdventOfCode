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

// See if any neighbors have a lower risk score than or equal risk score than me,
// if not then I'm at risk.
const isRisk = (grid, x, y) =>
  0 == neighbors(grid, x, y).filter(([i, j]) => grid[i][j] <= grid[x][y]).length;

riskSum = 0;
_.each(_.range(grid.length), x => (
  _.each(_.range(grid[0].length), y => (
    riskSum += isRisk(grid, x, y) ? grid[x][y] + 1 : 0))));

console.log(riskSum);
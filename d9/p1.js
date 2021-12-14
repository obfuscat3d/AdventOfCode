const _ = require('underscore');
const fs = require('fs');

const FILE = 'd9/input';

const raw_data = fs.readFileSync(FILE, 'utf8');
grid = raw_data.split('\n').map((row) => row.split('').map((point) => parseInt(point)));

function getNeighbors(grid, x, y) {
  candidates = [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]];
  return _.filter(candidates, (xy) => xy[0] >= 0 && xy[0] < grid.length && xy[1] >= 0 && xy[1] < grid[x].length);
}

function isRisk(grid, x, y) {
  return getNeighbors(grid, x, y).filter((xy) => grid[xy[0]][xy[1]] <= grid[x][y]).length == 0;
}

riskSum = 0;
for (let x = 0; x < grid.length; x++) {
  for (let y = 0; y < grid[x].length; y++) {
    if (isRisk(grid, x, y)) {
      riskSum += grid[x][y] + 1;
    }
  }
}

console.log(riskSum);
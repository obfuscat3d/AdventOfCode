const _ = require('underscore');
const fs = require('fs');

const FILE = 'd11/input';

const raw_data = fs.readFileSync(FILE, 'utf8');
grid = raw_data.split('\n').map((row) => row.split('').map((point) => parseInt(point)));

function getNeighbors(grid, x, y) {
  candidates = _.flatten([-1, 0, 1].map((a) => [-1, 0, 1].map((b) => [x + a, y + b])), 1)
  candidates = candidates.filter((xy) => (xy[0] != x || xy[1] != y));
  return _.filter(candidates, (xy) => xy[0] >= 0 && xy[0] < grid.length && xy[1] >= 0 && xy[1] < grid[x].length);
}

flashCount = 0;

function step(grid) {
  flashed = [];
  flash_queue = [];
  for (let i = 0; i < grid.length; i++) {
    for (let j = 0; j < grid[i].length; j++) {
      if (grid[i][j] >= 9) {
        flash_queue.push([i, j].join(','));
      }
    }
  }

  while (flash_queue.length) {
    cur = flash_queue.pop();
    if (!_.contains(flashed, cur)) {
      flashed.push(cur);
      flashCount++;
      xy = cur.split(',').map((n) => parseInt(n));
      _.each(getNeighbors(grid, xy[0], xy[1]), (n) => {
        if (++grid[n[0]][n[1]] >= 9) {
          flash_queue.push(n.join(','));
        }
      });
    }
  }

  for (let i = 0; i < grid.length; i++) {
    for (let j = 0; j < grid[i].length; j++) {
      grid[i][j]++;
    }
  }

  _.each(flashed, (e) => {
    [x, y] = e.split(',').map(n => parseInt(n));
    grid[x][y] = 0;
  });

}

function printGrid(grid) {
  for (let x in grid) {
    for (let y in grid[x]) {
      process.stdout.write(grid[x][y].toString()+' ');
    }
    process.stdout.write('\n');
  }
  process.stdout.write('\n');
}

_.each(_.range(100),n => step(grid));
console.log(flashCount);
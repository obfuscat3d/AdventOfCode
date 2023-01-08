// https://adventofcode.com/day/11

const _ = require('underscore');
const fs = require('fs');

const FILE = 'd11/input';

const raw_data = fs.readFileSync(FILE, 'utf8');
grid = raw_data.split('\n').map((row) => row.split('').map((point) => parseInt(point)));

// Get neighbors on a 2D grid.
const neighbors = (grid, x, y, diagonal = false) =>
  _.flatten([-1, 0, 1].map(a => [-1, 0, 1].map(b => [x + a, y + b])), 1) // get an array of coords
    .filter(([i, j]) => (
      i >= 0 && j >= 0 && i < grid.length && j < grid.length && // filter so they're valid coords
      (i != x || j != y) && // exclude self
      (diagonal || i == x || y == j))); // optionally exclude diagonal

// Convert between [x,y] coords and an int, handy for storing in hashmaps
// Note that the coords need to be less than 2^16
const xy = (coordArr) => (coordArr[0] << 16) + coordArr[1];
const yx = (coord) => [coord >> 16, coord & ((1 << 16) - 1)];

// Sort of a mess of a function that could be split up
function step(grid) {
  flashed = []; // Who has flashed this step?
  flash_queue = []; // Queue of octopi that need to flash

  // First, fine all the octopi with a score of 9 and queue them for flashing
  _.each(_.range(grid.length), x => (
    _.each(_.range(grid[0].length), y => {
      if (grid[x][y] >= 9) flash_queue.push(xy([x, y]));
    })));

  // Flash the ones in the queue and keep adding any new
  // octopi to the queue if they need to flash this step
  while (flash_queue.length) {
    cur = flash_queue.pop();
    if (!_.contains(flashed, cur)) {
      flashed.push(cur);
      [x, y] = yx(cur);
      _.each(neighbors(grid, x, y, true), ([i, j]) => {
        if (++grid[i][j] >= 9) {
          flash_queue.push(xy([i, j]));
        }
      });
    }
  }

  // Everyone's flashed, now increment all the energy levels
  _.each(_.range(grid.length), x => (
    _.each(_.range(grid[0].length), y => (
      grid[x][y]++
    ))));

  // And reset the flashers back to zero
  _.each(flashed, (e) => {
    [x, y] = yx(e);
    grid[x][y] = 0;
  });
}

for (let i = 1; _.some(_.flatten(grid)); i++) {
  step(grid);
  // The answer is whatever's printed last
  console.log(i);
}

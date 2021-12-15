// https://adventofcode.com/2021/day/11

const _ = require('underscore');
const fs = require('fs');
const µ = require('../../utils');

const FILE = '2021/d11/input';

const raw_data = fs.readFileSync(FILE, 'utf8');
grid = raw_data.split('\n').map((row) => row.split('').map(Number));

flashCount = 0;

// Mess of a function that could be split up
function step(grid) {
  flashed = []; // Who has flashed this step?
  flash_queue = []; // Queue of octopi that need to flash

  // First, fine all the octopi with a score of 9 and queue them for flashing
  _.each(_.range(grid.length), x => (
    _.each(_.range(grid[0].length), y => {
      if (grid[x][y] >= 9) flash_queue.push(µ.xy([x, y]));
    })));

  // Flash the ones in the queue and keep adding any new
  // octopi to the queue if they need to flash this step
  while (flash_queue.length) {
    cur = flash_queue.pop();
    if (!_.contains(flashed, cur)) {
      flashCount++;
      flashed.push(cur);
      [x, y] = µ.yx(cur);
      _.each(µ.neighbors(grid, x, y, true), ([i, j]) => {
        if (++grid[i][j] >= 9) {
          flash_queue.push(µ.xy([i, j]));
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
    [x, y] = µ.yx(e);
    grid[x][y] = 0;
  });
}

_.each(_.range(100), n => step(grid));
console.log(flashCount);
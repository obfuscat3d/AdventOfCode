// https://adventofcode.com/day/5

const _ = require('underscore');
const fs = require('fs');

const SIZE = 1000;
const FILE = 'd5/input';

// There has to be a better way to initialize a 2D array
grid = _.range(SIZE).map(a => _.range(SIZE).map((b) => 0));

const raw_data = fs.readFileSync(FILE, 'utf8');
lines = raw_data.split('\n').map(s => s.match(/\d+/g).map(Number));

let count = 0;
_.each(lines, l => {
  [x1, y1, x2, y2] = l;
  // To be honest, I like this implementation a lot more
  // than what I did in the first problem.
  steps = Math.max(Math.abs(x1 - x2), Math.abs(y2 - y1));
  dx = x1 == x2 ? 0 : (x1 < x2 ? 1 : -1);
  dy = y1 == y2 ? 0 : (y1 < y2 ? 1 : -1);
  for (let i = 0; i <= steps; i++) {
    if (++grid[x1 + i * dx][y1 + i * dy] == 2) {
      count++;
    }
  }
});

console.log(count);
// https://adventofcode.com/2021/day/5

const _ = require('underscore');
const fs = require('fs');

const SIZE = 1000;
const FILE = '2021/d5/input';

// There has to be a better way to initialize a 2D array
grid = _.range(SIZE).map((a) => _.range(SIZE).map((b) => 0));

const raw_data = fs.readFileSync(FILE, 'utf8');
lines = raw_data.split('\n').map((s) => s.match(/\d+/g).map((n) => parseInt(n)));

let count = 0;
_.each(lines, (l) => {
  [x1, y1, x2, y2] = l;
  [x1, x2] = x1 < x2 ? [x1, x2] : [x2, x1];
  [y1, y2] = y1 < y2 ? [y1, y2] : [y2, y1];
  if (x1 == x2 || y1 == y2) {
    for (let i = x1; i <= x2; i++) {
      for (let j = y1; j <= y2; j++) {
        grid[i][j]++;
        if (grid[i][j] == 2) {
          count++;
        }
      }
    }
  }
});

console.log(count);
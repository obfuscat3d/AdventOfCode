// https://adventofcode.com/day/17

const _ = require('underscore');
const fs = require('fs');

const isHit = (x, y) => 155 <= x && x <= 182 && -117 <= y && y <= -67;

const best_height = (dx, dy) => {
  let x = 0, y = 0, best = 0;
  while (y >= -117) {
    if (isHit(x, y)) {
      return best;
    }
    x = dx ? x + dx-- : x;
    y += dy--;
    best = Math.max(best, y);
  }
  return -1;
};

count = 0;
best = 0;
_.each(_.range(0, 400), dx => {
  _.each(_.range(-117, 500), dy => {
    if ((candidate = best_height(dx, dy)) >= 0) {
      count++;
      best = Math.max(best, candidate);
    }
  });
});

console.log(best, count);
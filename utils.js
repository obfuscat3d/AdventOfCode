// Commonly used functions it's handy to have around. By convention
// I tend to use µ as the import variable, as it's the first letter
// of my surname. If I were Greek. And didn't capitalize names.

const _ = require('underscore');

// Get neighbors on a 2D grid.
const neighbors = (grid, x, y, diagonal = false) =>
  _.flatten([-1, 0, 1].map(a => [-1, 0, 1].map(b => [x + a, y + b])), 1) // get an array of coords
    .filter(([i, j]) => (
      i >= 0 && j >= 0 && i < grid.length && j < grid.length && // filter so they're valid coords
      (i != x || j != y) && // exclude self
      (diagonal || i == x || y == j))); // optionally exclude diagonal

// make a 2D grid
const makeGrid = (x, y, fill = 0) =>
  _.range(x).map(() => _.range(y).map(() => fill));

// Convert between [x,y] coords and an int, handy for storing in hashmaps
// Note that the coords need to be less than 2^16
const xy = (coordArr) => (coordArr[0]<<16) + coordArr[1];
const yx = (coord) => [coord>>16, coord&((1<<16)-1)];

// This comes up a lot in debugging
const printGrid = (grid) => {
  _.each(grid, n => console.log(n.join('')));
}

module.exports = {
  neighbors: neighbors,
  makeGrid: makeGrid,
  xy: xy,
  yx: yx,
  printGrid: printGrid,
}

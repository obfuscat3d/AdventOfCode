// https://adventofcode.com/day/15

const _ = require('underscore');
const fs = require('fs');
const { MinPriorityQueue } = require('@datastructures-js/priority-queue');

FILE = 'd15/input'

const raw_data = fs.readFileSync(FILE, 'utf8');
tmp_grid = raw_data.split('\n').map(l => l.split('').map(Number));

// Get neighbors on a 2D grid.
const neighbors = (grid, x, y, diagonal = false) =>
  _.flatten([-1, 0, 1].map(a => [-1, 0, 1].map(b => [x + a, y + b])), 1) // get an array of coords
    .filter(([i, j]) => (
      i >= 0 && j >= 0 && i < grid.length && j < grid.length && // filter so they're valid coords
      (i != x || j != y) && // exclude self
      (diagonal || i == x || y == j))); // optionally exclude diagonal

// Problem 2 has us repeat the grid from problem one while incrementing
// the risk factor along the way. Also, we're assuming a square grid.
t_size = tmp_grid.length;
grid = _.range(5 * t_size).map((x) => (
  _.range(5 * t_size).map((y) => (
    tmp_grid[x % t_size][y % t_size] +
    Math.floor(x / t_size) + Math.floor(y / t_size)
    - 1) % 9 + 1) // This is a hacky little way to loop 9 -> 1
));

// Use Djikstra's algorithm to traverse the map.
//
// done tracks whether the quickest path to x,y is known
done = _.range(grid.length).map(() => _.range(grid.length).map(() => 0));
// cost is the current cost to get to x,y and initialized higher than anything we'll see
cost = _.range(grid.length).map(() => _.range(grid.length).map(() => 1 << 16));
// The cost to get to the start is always zero
cost[0][0] = 0;

pq = new MinPriorityQueue();
pq.enqueue([0, 0], 0);

// Main Djikstra loop
while (!done[grid.length - 1][grid.length - 1]) {
  let [x, y] = pq.dequeue().element;
  done[x][y] = 1;
  _.each(neighbors(grid, x, y), ([i, j]) => {
    let alt = cost[x][y] + grid[i][j];
    if (!done[i][j] && alt < cost[i][j]) {
      cost[i][j] = alt;
      pq.enqueue([i, j], alt);
    }
  });
}

console.log(cost[grid.length - 1][grid.length - 1]);
// https://adventofcode.com/2021/day/15

const _ = require('underscore');
const fs = require('fs');
const { MinPriorityQueue } = require('@datastructures-js/priority-queue');
const µ = require('../../utils')

FILE = '2021/d15/input'

const raw_data = fs.readFileSync(FILE, 'utf8');
grid = raw_data.split('\n').map(l => l.split('').map(Number));

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
  _.each(µ.neighbors(grid, x, y), ([i, j]) => {
    let alt = cost[x][y] + grid[i][j];
    if (!done[i][j] && alt < cost[i][j]) {
      cost[i][j] = alt;
      pq.enqueue([i, j], alt);
    }
  });
}

console.log(cost[grid.length - 1][grid.length - 1]);

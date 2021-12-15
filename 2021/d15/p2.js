// https://adventofcode.com/2021/day/15

const _ = require('underscore');
const fs = require('fs');
const { MinPriorityQueue } = require('@datastructures-js/priority-queue');

FILE = '2021/d15/input'

const raw_data = fs.readFileSync(FILE, 'utf8');
tmp_grid = raw_data.split('\n').map((l) => l.split('').map((n) => parseInt(n)));

t_size = tmp_grid.length;
grid = _.range(5 * t_size).map((x) => (
  _.range(5 * t_size).map((y) => {
    v = tmp_grid[x % t_size][y % t_size] + Math.floor(x / t_size) + Math.floor(y / t_size);
    return v > 9 ? v - 9 : v;
  })
));

// Handy function to generate non-diagonal neighbors in a grid
neighbors = (x, y) => [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]].filter((a) => a[0] >= 0 && a[1] >= 0 && a[0] < grid.length && a[1] < grid.length);

// Use Djikstra's algorithm to traverse the map.
// https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
//
// done tracks whether the quickest path to x,y is known
done = _.range(grid.length).map(() => _.range(grid.length).map(() => 0));
// cost is the current cost to get to x,y and initialized higher than anything we'll see
cost = _.range(grid.length).map(() => _.range(grid.length).map(() => 1 << 16));
// The cost to get to the start is always zero
cost[0][0] = 0;

pq = new MinPriorityQueue();
pq.enqueue([0, 0], 0);

while (!done[grid.length - 1][grid.length - 1]) {
  let [x, y] = pq.dequeue().element;
  done[x][y] = 1;
  _.each(neighbors(x, y), (n) => {
    [i, j] = n;
    let alt = cost[x][y] + grid[i][j];
    if (!done[i][j] && alt < cost[i][j]) {
      cost[i][j] = alt;
      pq.enqueue([i, j], alt);
    }
  });
}

console.log(cost[grid.length - 1][grid.length - 1]);

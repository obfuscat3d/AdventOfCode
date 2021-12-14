// https://adventofcode.com/2021/day/9

const _ = require('underscore');
const fs = require('fs');

const FILE = 'd9/input';

const raw_data = fs.readFileSync(FILE, 'utf8');
grid = raw_data.split('\n').map((row) => row.split('').map((point) => parseInt(point)));

function getNeighbors(grid, x, y) {
  candidates = [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]];
  return _.filter(candidates, (xy) => xy[0] >= 0 && xy[0] < grid.length && xy[1] >= 0 && xy[1] < grid[x].length);
}

function isRisk(grid, x, y) {
  return getNeighbors(grid, x, y).filter((xy) => grid[xy[0]][xy[1]] <= grid[x][y]).length == 0;
}

function basinSize(grid, x, y) {
  // And fuck it, we'll just use strings because it makes checking equality easy.
  // This is so fucking ugly.
  size = 0;
  visited = [];
  stack = [[x, y].join(',')];
  while (stack.length) {
    current = stack.pop().split(',').map((n) => parseInt(n));
    visited.push(current.join(','));
    size++;
    n = getNeighbors(grid, current[0], current[1]);
    m = n.filter((xy) => {
      return (grid[xy[0]][xy[1]] != 9) && !_.contains(visited, xy.join(',')) && !_.contains(stack, xy.join(','))
    });
    stack = stack.concat(m.map((xy) => xy.join(',')));
  }
  return size;
}

basins = []
for (let x = 0; x < grid.length; x++) {
  for (let y = 0; y < grid[x].length; y++) {
    // Fun fact, this will work from any square. We use low points to avoid dupes.
    if (isRisk(grid, x, y)) {
      basins.unshift(basinSize(grid, x, y));
    }
  }
}

basins.sort((a,b) => (a-b));
console.log(basins.pop() * basins.pop() * basins.pop());
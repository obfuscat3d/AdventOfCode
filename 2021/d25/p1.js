const _ = require('underscore');
const fs = require('fs');

// return true if needs to run again
function step(grid) {
  height = grid.length;
  width = grid[0].length;

  again = false;

  right_grid = _.range(height).map(q => _.range(width).map(i => '.'));
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      if (grid[y][x] == '>' && grid[y][(x + 1) % width] == '.') {
        right_grid[y][(x + 1) % width] = '>';
        again = true;
      } else if (grid[y][x] == '>') {
        right_grid[y][x] = '>';
      }
    }
  }

  down_grid = _.range(height).map(y => _.range(width).map(x => right_grid[y][x]));
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      if (grid[y][x] == 'v' && down_grid[(y + 1) % height][x] == '.' && grid[(y + 1) % height][x] != 'v') {
        down_grid[(y + 1) % height][x] = 'v';
        again = true;
      } else if (grid[y][x] == 'v') {
        down_grid[y][x] = 'v';
      }
    }
  }

  return [down_grid, again];
}

function part1(grid) {
  i = 0, again = true;
  while (again) {
    [grid, again] = step(grid);
    i++;
  }
  return i;
}

const raw_data = fs.readFileSync('d25/input', 'utf8');
let grid = raw_data.split('\n').map(line => line.split(''));
console.log(part1(grid));
const _ = require('underscore');
const fs = require('fs');

const FILE = 'd13/input';

function pg(g) {
  for (let y = 0; y < g[0].length; y++) {
    for (let x = 0; x < g.length; x++) {
      process.stdout.write(g[x][y].toString());
    }
    process.stdout.write('\n');
  }
  process.stdout.write('\n');
  process.stdout.write('\n');
}

const raw_data = fs.readFileSync(FILE, 'utf8');
[lines, instructions] = raw_data.split('\n\n');
points = lines.split('\n').map((l) => l.split(',').map((n) => parseInt(n)));
[width, height] = [1+Math.max(..._.pluck(points, 0)), 1+Math.max(..._.pluck(points, 1))];

grid = Array(width).fill(0).map(x => new Array(height).fill(0));
_.each(points, p => grid[p[0]][p[1]] = 1);

instructions = instructions.split('\n');
_.each(instructions, (i) => {
  [axis, line] = i.substring(11).split('=');
  line = parseInt(line);
  if (axis == 'y') { // Folding "up"
    for (let y = 0; y < line; y++) {
      for (let x = 0; x < grid.length; x++) {
        grid[x][y] |= grid[x][2 * line - y];
        grid[x][2 * line - y] = 0;
      }
    }
  }
  if (axis == 'x') { // Folding "up"
    for (let x = 0; x < line; x++) {
      for (let y = 0; y < grid[0].length; y++) {
        grid[x][y] |= grid[2*line-x][y];
        grid[2 * line - x][y] = 0;
      }
    }
  }
})

pg(grid);

console.log(_.compact(_.flatten(grid)).length);

// https://adventofcode.com/2021/day/2

const _ = require('underscore');
const fs = require('fs');

const raw_data = fs.readFileSync('d2/input', 'utf8');
const data = _.toArray(raw_data.split(/\n/));

let aim = 0, forward = 0, depth = 0;
for (i in data) {
  let [dir, val] = data[i].split(' ');
  val = parseInt(val);
  if (dir == 'forward') {
    forward += val;
    depth += aim * val;
  } else {
    aim += dir == 'up' ? -val : val;
  }
}

console.log(forward * depth);
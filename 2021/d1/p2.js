// https://adventofcode.com/2021/day/1

const _ = require('underscore');
const fs = require('fs');

const raw_data = fs.readFileSync('2021/d1/input', 'utf8');
const data = _.toArray(raw_data.split(/\s/)).map(Number);

let incr = _.countBy(_.range(0, data.length - 3), i => {
  return data.slice(i, i+3).reduce((a, b) => a + b, 0) < data.slice(i+1, i+4).reduce((a, b) => a + b, 0);
});

console.log(incr[true]);
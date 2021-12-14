const _ = require('underscore');
const fs = require('fs');

const FILE = 'd7/input';

const raw_data = fs.readFileSync(FILE, 'utf8');
pos = raw_data.split(',').map((n) => parseInt(n)).sort();
b = _.range(Math.max(...pos)).map((guess) => {
  return pos.map((p) => {
    d = Math.abs(p - guess);
    return d*(d+1)/2;
  }).reduce((a, b) => a + b, 0);
});

console.log(Math.min(...b));

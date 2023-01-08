// https://adventofcode.com/day/10

const _ = require('underscore');
const fs = require('fs');

const FILE = 'd10/input';
const CHARS = {
  '(': ')',
  '[': ']',
  '{': '}',
  '<': '>'
}
const POINTS = {
  '(': 1,
  '[': 2,
  '{': 3,
  '<': 4
}

const raw_data = fs.readFileSync(FILE, 'utf8');
points = raw_data.split('\n').map((l) => {
  stack = [];
  for (let i in l) {
    if (l[i] in CHARS) {
      stack.push(l[i]);
    } else {
      if (l[i] != CHARS[stack.pop()]) {
        return 0;
      }
    }
  }
  return _.reduceRight(stack, (a,b) => 5*a + POINTS[b], 0);
});

points = _.compact(points);
points.sort((a, b) => (a - b));
console.log(points[Math.floor(points.length/2)]);

const _ = require('underscore');
const fs = require('fs');

const FILE = 'd10/input';
const CHARS = {
  '(':')',
  '[':']',
  '{':'}',
  '<':'>'
}
const POINTS = {
  ')': 3,
  ']': 57,
  '}': 1197,
  '>': 25137
}

const raw_data = fs.readFileSync(FILE, 'utf8');
points = raw_data.split('\n').map((l) => {
  stack = [];
  for (let i in l) {
    if (l[i] in CHARS) {
      stack.push(l[i]);
    } else {
      if (l[i] != CHARS[stack.pop()]) {
        return POINTS[l[i]];
      }
    }
  }
  return 0;
});

console.log(points.reduce((a,b) => a+b,0));
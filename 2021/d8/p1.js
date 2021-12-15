// https://adventofcode.com/2021/day/8

const _ = require('underscore');
const fs = require('fs');

const FILE = '2021/d8/input';

const raw_data = fs.readFileSync(FILE, 'utf8');
// Get the outputs
outputs = raw_data.split('\n').map((s) => s.split('|')[1].trim());
// Count how many 2, 3, 4, and 7 character outputs there are
a = outputs.map((o) => 
  o.split(' ').filter((s) => _.contains([2, 3, 4, 7], s.length)).length
);

console.log(a.reduce((a,b) => a+b,0));
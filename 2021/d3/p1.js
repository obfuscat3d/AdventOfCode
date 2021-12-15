// https://adventofcode.com/2021/day/3

const _ = require('underscore');
const fs = require('fs');

const NUM_BITS = 12; 
const FILE = '2021/d3/input';

const raw_data = fs.readFileSync(FILE, 'utf8');
const data = _.toArray(raw_data.split(/\s/)).map((n) => parseInt(n, 2));

let gamma=0, epsilon=0;

for (let i=0; i < NUM_BITS; i++) {
  bits = _.countBy(data.map((n) => (n & 1<<i) ? 1 : 0));
  gamma += (bits[1] < data.length/2) ? 0 : 1<<i;
}

epsilon = ((1<<NUM_BITS)-1) ^ gamma;

console.log('Gamma: ' + gamma);
console.log('Epsilon: ' + epsilon);
console.log('Power: ' + gamma*epsilon);

// https://adventofcode.com/day/3

const _ = require('underscore');
const fs = require('fs');

const NUM_BITS = 12;
const FILE = 'd3/input';

const raw_data = fs.readFileSync(FILE, 'utf8');
const data = _.toArray(raw_data.split(/\s/)).map((n) => parseInt(n, 2));

let gamma = 0, epsilon = 0;

_.each(_.range(NUM_BITS), (n) => {
  // bits is an array = [number_of_zeros, number_of_ones], so bits[1] = number of ones
  bits = _.countBy(data.map((n) => (n & 1 << i) ? 1 : 0));
  gamma += (bits[1] < data.length / 2) ? 0 : 1 << i;
});

// epsilon is just gamma with all the bits flipped
epsilon = ((1 << NUM_BITS) - 1) ^ gamma;

console.log('Gamma: ' + gamma);
console.log('Epsilon: ' + epsilon);
console.log('Power: ' + gamma * epsilon);

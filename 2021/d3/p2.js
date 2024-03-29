// https://adventofcode.com/day/3

const _ = require('underscore');
const fs = require('fs');

const NUM_BITS = 12;
const FILE = 'd3/input';

const raw_data = fs.readFileSync(FILE, 'utf8');
const data = _.toArray(raw_data.split(/\s/)).map((n) => parseInt(n, 2));

let oxygen = data;
// Keep most common, if tied, keep 1s
for (let i = NUM_BITS - 1; i >= 0 && oxygen.length > 1; i--) {
  // bits is an array = [number_of_zeros, number_of_ones], so bits[1] = number of ones
  bits = _.countBy(oxygen.map((n) => (n & 1 << i) ? 1 : 0));
  if (bits[0] <= bits[1]) {
    oxygen = _.filter(oxygen, (n) => n & 1 << i);
  } else {
    oxygen = _.filter(oxygen, (n) => !(n & 1 << i));
  }
}

let scrubber = data;
// Keep least common, if tied, keep 0s
for (let i = NUM_BITS - 1; i >= 0 && scrubber.length > 1; i--) {
  // bits is an array = [number_of_zeros, number_of_ones], so bits[1] = number of ones
  bits = _.countBy(scrubber.map((n) => (n & 1 << i) ? 1 : 0));
  if (bits[0] > bits[1]) {
    scrubber = _.filter(scrubber, (n) => n & 1 << i);
  } else {
    scrubber = _.filter(scrubber, (n) => !(n & 1 << i));
  }
}

console.log(oxygen);
console.log(scrubber);

const _ = require('underscore');
const fs = require('fs');

const ROTATIONS = [
  (x, y, z) => [x, y, z],
  (x, y, z) => [x, -z, y],
  (x, y, z) => [x, -y, -z],
  (x, y, z) => [x, z, -y],
  (x, y, z) => [-x, -y, z],
  (x, y, z) => [-x, -z, -y],
  (x, y, z) => [-x, y, -z],
  (x, y, z) => [-x, z, y],
  (x, y, z) => [y, x, -z],
  (x, y, z) => [y, z, x],
  (x, y, z) => [y, -x, z],
  (x, y, z) => [y, -z, -x],
  (x, y, z) => [-y, -x, -z],
  (x, y, z) => [-y, z, -x],
  (x, y, z) => [-y, x, z],
  (x, y, z) => [-y, -z, x],
  (x, y, z) => [z, -x, -y],
  (x, y, z) => [z, y, -x],
  (x, y, z) => [z, x, y],
  (x, y, z) => [z, -y, x],
  (x, y, z) => [-z, -x, y],
  (x, y, z) => [-z, -y, -x],
  (x, y, z) => [-z, x, -y],
  (x, y, z) => [-z, y, x],
];

function isMatch(s0_set, s1, rot, offset) {
  c = 0;
  for (let i = 0; i < s1.length && ((12 - c) < (s1.length - i + 1)); i++) {
    if (s0_set.has(offset(...rot(...s1[i])).toString())) {
      if (++c >= 12) return true;
    };
  }
  return false;
}

// If s0 and s1 overlap, return s1 and the scanner location in s0's coordinates
function align(s0, s1) {
  s0_set = new Set(s0.map(x => x.toString())); // String for quicker hashing
  for (i in ROTATIONS) { // For each rotation...
    rot = ROTATIONS[i];
    for (j in s1) { // For each point in s1 in the rotation...
      c1 = rot(...s1[j]);
      for (k in s0) { // For every point in s0 (no rotation needed)...
        c0 = s0[k];
        offset = (x, y, z) => [x + c0[0] - c1[0], y + c0[1] - c1[1], z + c0[2] - c1[2]];
        if (isMatch(s0_set, s1, rot, offset)) { // Does the proposed rotation and offset produce a match?
          return [s1.map(coord => offset(...(rot(...coord)))), offset(0, 0, 0)];
        }
      }
    }
  }
  return [null, null]; // default if no match. boo.
};

const manhattan = (a, b) => Math.abs(a[0] - b[0]) + Math.abs(a[1] - b[1]) + Math.abs(a[2] - b[2]);

const raw_data = fs.readFileSync('2021/d19/input', 'utf8');
scanner_data = raw_data.split('\n\n').map(s => s.split('\n').slice(1).map(l => l.split(',').map(Number)));

// Process data, final = array of beacon tuples in scanner 0's coordinates
[final, scanner_data] = [scanner_data[0], scanner_data.slice(1)];
scanners = [[0, 0, 0]] // Needed for part 2
while (scanner_data.length) {
  _.each(scanner_data, sd => {
    [match, scanner_loc] = align(final, sd);
    if (match) {
      final = final.concat(match);
      scanners.push(scanner_loc);
      final = _.uniq(final, false, x => x.toString());
      sd.length = 0;
    }
  });
  scanner_data = _.filter(scanner_data, x => x.length);
}

// Part 1
console.log(final.length);

// Part 2
mm = 0;
_.each(scanners, c0 => _.each(scanners, c1 => mm = Math.max(mm, manhattan(c0, c1))));
console.log(mm);
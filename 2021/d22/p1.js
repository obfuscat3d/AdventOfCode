const _ = require('underscore');
const fs = require('fs');

const raw_data = fs.readFileSync('2021/d22/input', 'utf8');
instructions = raw_data.split('\n').map(a =>
  [a.substr(0, 2) == 'on', [...a.substr(3).matchAll(/-?\d+/g)].map(b => parseInt(b[0]))])

const k = (x, y, z) => [x, y, z].join(',');

universe = new Map();
_.each(instructions, i => {
  for (let x = i[1][0]; x <= i[1][1]; x++)
    for (let y = i[1][2]; y <= i[1][3]; y++)
      for (let z = i[1][4]; z <= i[1][5]; z++)
        universe.set(k(x, y, z), i[0]);
});

counter = 0;
universe.forEach(value => { counter += value; });
console.log(counter);
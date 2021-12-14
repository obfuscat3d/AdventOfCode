const _ = require('underscore');
const fs = require('fs');

const FILE = 'd8/input';

// Messy, but it works.
function getDigitMap(numbers) {
  numbers = numbers.map((n) => n.split(''));
  digitMap = {}
  digitMap[1] = numbers.filter((n) => n.length == 2)[0];
  digitMap[7] = numbers.filter((n) => n.length == 3)[0];
  digitMap[4] = numbers.filter((n) => n.length == 4)[0];
  digitMap[8] = numbers.filter((n) => n.length == 7)[0];
  digitMap[9] = numbers.filter((n) =>
    (n.length == 6 && _.difference(n, _.union(digitMap[7], digitMap[4])).length == 1))[0];
  numbers = _.difference(numbers, _.values(digitMap));
  digitMap[6] = numbers.filter((n) => n.length == 6 && _.difference(digitMap[1], n).length == 1)[0];
  numbers = _.difference(numbers, _.values(digitMap));
  digitMap[0] = numbers.filter((n) => n.length == 6)[0];
  numbers = _.difference(numbers, _.values(digitMap));
  digitMap[2] = numbers.filter((n) => _.difference(n, digitMap[9]).length == 1)[0];
  numbers = _.difference(numbers, _.values(digitMap));
  digitMap[3] = numbers.filter((n) => _.difference(digitMap[1], n).length == 0)[0];
  numbers = _.difference(numbers, _.values(digitMap));
  digitMap[5] = numbers[0];
  ret = {}
  for (i in digitMap) {
    ret[digitMap[i].sort().join('')] = parseInt(i);
  }
  return ret;
}

const raw_data = fs.readFileSync(FILE, 'utf8');
data = raw_data.split('\n');
a = data.map((o) => {
  digitMap = getDigitMap(o.match(/[a-z]+/g));
  o = o.split('| ')[1].split(' ').map((s) => digitMap[s.split('').sort().join('')]);
  return o.reduce((a,b) => a*10+b, 0);
});

console.log(a.reduce((a, b) => a + b, 0));
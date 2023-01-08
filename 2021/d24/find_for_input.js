const _ = require('underscore');
const fs = require('fs');

function run(input, biggest = true) {
  final = Array(14);
  stack = [];

  for (let i = 0; i < 14; i += 1) {
    x_add = parseInt(input[18 * i + 5].split(' ')[2]);
    y_add = parseInt(input[18 * i + 15].split(' ')[2]);
    if (x_add > 0) {
      stack.push([y_add, i]);
    } else {
      s = stack.pop();
      [y_add, y_index] = [s[0], s[1]];
      if (biggest) {
        to_add = 9;
        while (to_add + y_add + x_add > 9) to_add--;
      } else {
        to_add = 1;
        while (to_add + y_add + x_add < 1) to_add++;
      }
      final[y_index] = to_add;
      final[i] = to_add + y_add + x_add;
    }
  }
  return final.join('');
}

const raw_data = fs.readFileSync('d24/input', 'utf8');
const input = raw_data.split('\n');

console.log('Biggest: ', run(input));
console.log('Smallest: ', run(input, false));

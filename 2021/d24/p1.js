const _ = require('underscore');
const fs = require('fs');

function run(program, input_buffer) {
  let mem = { 'w': 0, 'x': 0, 'y': 0, 'z': 0 }

  program.forEach(i => {
    a = i[4];
    if (['w', 'x', 'y', 'z'].indexOf(i[6]) != -1) {
      b = mem[i[6]];
    } else {
      b = parseInt(i.substr(6));
    }
    switch (i.substr(0, 3)) {
      case 'inp':
        mem[a] = parseInt(input_buffer[0]);
        input_buffer = input_buffer.substr(1);
        break;
      case 'add':
        mem[a] = mem[a] + b;
        break;
      case 'mul':
        mem[a] = mem[a] * b;
        break;
      case 'div':
        mem[a] = Math.floor(mem[a] / b);
        break;
      case 'mod':
        mem[a] = mem[a] % b;
        break;
      case 'eql':
        mem[a] = mem[a] == b ? 1 : 0;
        break;
    }
  });

  return mem['z'] == 0;
}

const raw_data = fs.readFileSync('d24/input', 'utf8');
const program = raw_data.split('\n');
console.log(run(program, '95299897999897'));
const _ = require('underscore');

algorithm = '';

for (let i = 0; i < 1 << 9; i++) {
  lit = _.range(9).reduce((a, b) => a + (i & (1 << b) ? 1 : 0), 0);
  if (i & (1 << 4))
    algorithm += (lit == 3 || lit == 4) ? '#' : '.';
  else
    algorithm += (lit == 3) ? '#' : '.';
}

console.log(algorithm);
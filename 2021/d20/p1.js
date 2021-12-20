const _ = require('underscore');
const fs = require('fs');

const k = (x, y) => [x, y].join(',');
const neighbors = (x, y) => _.flatten([-1, 0, 1].map(i => [-1, 0, 1].map(j => [x + i, y + j])), 1);

function parseImage(image_text) {
  image = new Map();
  for (let [x, row] of image_text.split('\n').entries())
    for (let [y, px] of row.split('').entries())
      image.set(k(x, y), px);
  return [image, [0, 0, image_text.split('\n').length - 1, image_text.split('\n')[0].length - 1]]
}

function calcNext(algorithm, image, iter, x, y) {
  blank = iter % 2 == 0 ? '.' : algorithm[0];
  algorithm_index_str = neighbors(x, y).map(c => image.get(k(c[0], c[1])) ?? blank).join('')
  algorithm_index = parseInt(algorithm_index_str.replace(/#/g, '1').replace(/\./g, '0'), 2);
  return algorithm[algorithm_index];
}

function step(algorithm, image, bounds, iter) {
  [minX, minY, maxX, maxY] = bounds;
  next_image = new Map();
  for (let x = minX - 2; x <= maxX + 2; x++) // always exceed the bounds by 2 in all directions
    for (let y = minY - 2; y <= maxY + 2; y++)
      next_image.set(k(x, y), calcNext(algorithm, image, iter, x, y));
  return [next_image, [bounds[0] - 2, bounds[1] - 2, bounds[2] + 2, bounds[3] + 2]];
}

function run(algorithm, image, bounds, iterations) {
  [image, bounds] = _.range(iterations).reduce((a, b) => step(algorithm, a[0], a[1], b), [image, bounds]);
  console.log(_.countBy(Array.from(image.values())));
}

const raw_data = fs.readFileSync('2021/d20/input', 'utf8');
[algorithm, image_text] = raw_data.split(/\n\n/);
[image, bounds] = parseImage(image_text);

run(algorithm, image, bounds, 2); // Part 1
run(algorithm, image, bounds, 50); // Part 2
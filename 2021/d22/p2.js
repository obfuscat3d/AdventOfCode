const _ = require('underscore');
const fs = require('fs');

const line_overlap = (min0, max0, min1, max1) => [Math.max(min0, min1), Math.min(max0, max1)];
const volume = (b) => (b.x2 - b.x1 + 1) * (b.y2 - b.y1 + 1) * (b.z2 - b.z1 + 1);
const new_box = (x1, x2, y1, y2, z1, z2) => ({
  x1: x1, // = x min
  x2: x2, // = y max
  y1: y1,
  y2: y2,
  z1: z1,
  z2: z2
});

function overlap(box, boxes) {
  return boxes.map((b, i) => {
    [overlapMinX, overlapMaxX] = line_overlap(box.x1, box.x2, b.x1, b.x2);
    [overlapMinY, overlapMaxY] = line_overlap(box.y1, box.y2, b.y1, b.y2);
    [overlapMinZ, overlapMaxZ] = line_overlap(box.z1, box.z2, b.z1, b.z2);
    if (overlapMaxX - overlapMinX >= 0 &&
      overlapMaxY - overlapMinY >= 0 &&
      overlapMaxZ - overlapMinZ >= 0) {
      temp_box = new_box(overlapMinX, overlapMaxX, overlapMinY, overlapMaxY, overlapMinZ, overlapMaxZ);
      return volume(temp_box) - overlap(temp_box, boxes.slice(i + 1));
    } else {
      return 0; // No overlap
    }
  }).reduce((a, b) => a + b, 0);
}

function part2(instructions) {
  total_on = 0;
  boxes = [];
  // Go through the instruction in reverse and check for any previous overlap if "on"
  _.each(instructions.reverse(), i => {
    box = new_box(...i[1]);
    i[0] == 'on' && (total_on += volume(box) - overlap(box, boxes));
    boxes.push(box);
  })
  return total_on;
}

const raw_data = fs.readFileSync('2021/d22/input4', 'utf8');
instructions = raw_data.split('\n').map(a =>
  [a.substr(0, 2), [...a.substr(3).matchAll(/-?\d+/g)].map(b => parseInt(b[0]))])

console.log(part2(instructions));
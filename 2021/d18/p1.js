const _ = require('underscore');
const fs = require('fs');

class Node {
  parent = null;
  left = null;
  right = null;
  value = null;

  constructor(input, parent = null) {
    this.parent = parent;
    if (typeof input == 'number') {
      this.value = input;
    } else {
      this.left = input[0] instanceof Node ? input[0] : new Node(input[0], this);
      this.right = input[1] instanceof Node ? input[1] : new Node(input[1], this);
    }
  }

  split() {
    this.left = new Node(Math.floor(this.value / 2), this);
    this.right = new Node(Math.ceil(this.value / 2), this);
    this.value = null;
  }

  explode() {
    let p = this;
    while (p && p.farLeft().parent == this) p = p.parent;
    if (p) p.left.farRight().value += this.left.value;

    p = this;
    while (p && p.farRight().parent == this) p = p.parent;
    if (p) p.right.farLeft().value += this.right.value;

    this.value = 0;
    this.left = null;
    this.right = null;
  }

  farLeft() {
    let n = this;
    while (n.left) n = n.left;
    return n;
  }

  farRight() {
    let n = this;
    while (n.right) n = n.right;
    return n;
  }

  findNodeToExplode(depth = 4) {
    if (this.value !== null) return false; // Never explode a leaf
    if (depth == 0) return this; // Always explode max depth non-leaf
    return this.left.findNodeToExplode(depth - 1) || this.right.findNodeToExplode(depth - 1);
  }

  findNodeToSplit() {
    if (this.value !== null) return this.value > 9 ? this : null;
    return this.left.findNodeToSplit() || this.right.findNodeToSplit();
  }

  reduce() {
    let n;
    while (n = this.findNodeToExplode()) n.explode();
    if (n = this.findNodeToSplit()) {
      n.split();
      this.reduce();
    }
    return this;
  }

  add(x) {
    let n = new Node([this, x]);
    this.parent = n;
    n.right.parent = n;
    return n;
  }

  magnitude() {
    if (this.value !== null) return this.value;
    return 3 * this.left.magnitude() + 2 * this.right.magnitude();
  }
}

const raw_data = fs.readFileSync('d18/input', 'utf8');
numbers = raw_data.split(/\n/).map(l => JSON.parse(l));

// Part 1
blah = (new Node(numbers[0])).reduce();
for (let i = 1; i < numbers.length; i++)
  blah = blah.add(numbers[i]).reduce();
console.log(blah.magnitude());

// Part 2
max = 0;
_.each(numbers, i => _.each(numbers, j => {
  max = Math.max(max, new Node(i).add(j).reduce().magnitude());
  max = Math.max(max, new Node(j).add(i).reduce().magnitude());
}));
console.log(max);

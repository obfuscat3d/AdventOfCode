// https://adventofcode.com/day/12

const _ = require('underscore');
const fs = require('fs');

const FILE = 'd12/input';

graph = {}

const raw_data = fs.readFileSync(FILE, 'utf8');
_.each(raw_data.split(/\n/), (e) => {
  [a, b] = e.split('-');
  a in graph ? graph[a].push(b) : graph[a] = [b];
  b in graph ? graph[b].push(a) : graph[b] = [a];
});

function canRevisit(node) {
  return /^[A-Z]+$/.test(node);
}

// Simple DFS path counting straight out of freshman year.
// Only change from p1 is that we can visit one minor node twice,
// so we just track whether or not we've done that for the
// current path in hasRevisited
function countPaths(graph, node, path, hasRevisited) {
  if (node == 'start' && path.length) {
    return 0;
  }

  if (node == 'end') {
    return 1;
  }

  if (!canRevisit(node) && _.contains(path, node)) {
    if (!hasRevisited) {
      hasRevisited = true;
    } else {
      // Short circuit if we're just revisiting a minor node for the second time.
      return 0;
    }
  }

  return graph[node]
    .map(dest => countPaths(graph, dest, [...path, node], hasRevisited))
    .reduce((a, b) => a + b, 0);
}

console.log(countPaths(graph, 'start', [], false));
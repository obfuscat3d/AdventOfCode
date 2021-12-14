const _ = require('underscore');
const fs = require('fs');

const FILE = 'd12/input';

graph = {}

const raw_data = fs.readFileSync(FILE, 'utf8');
_.each(raw_data.split(/\n/), (e) => {
  [a, b] = e.split('-');
  _.contains(_.keys(graph), a) ? graph[a].push(b) : graph[a] = [b];
  _.contains(_.keys(graph), b) ? graph[b].push(a) : graph[b] = [a];
});

function canRevisit(node) {
  return /^[A-Z]+$/.test(node);
}

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
      return 0;
    }
  }

  return graph[node].map((dest) => countPaths(graph, dest, [...path, node], hasRevisited)).reduce((a, b) => a + b, 0);
}

console.log(countPaths(graph, 'start', [], false));
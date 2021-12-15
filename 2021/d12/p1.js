// https://adventofcode.com/2021/day/12

const _ = require('underscore');
const fs = require('fs');

const FILE = '2021/d12/input';

// Graph = { node1: [node2, node3, ...], ...}
graph = {}

const raw_data = fs.readFileSync(FILE, 'utf8');
_.each(raw_data.split(/\n/), (e) => {
  [a,b] = e.split('-');
  a in graph ? graph[a].push(b) : graph[a] = [b];
  b in graph ? graph[b].push(a) : graph[b] = [a];
});

function canRevisit(node) {
  return /^[A-Z]+$/.test(node);
}

// Simple DFS path counting straight out of freshman year.
function countPaths(graph, node, path) {
  if (node == 'start' && path.length) {
    return 0;
  }

  if (node == 'end') {
    return 1;
  }

  if (!canRevisit(node) && _.contains(path, node)) {
    return 0;
  }

  return graph[node].map(dest => countPaths(graph, dest, [...path, node])).reduce((a,b) => a+b,0);
}

console.log(countPaths(graph, 'start', []));
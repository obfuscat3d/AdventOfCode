// https://adventofcode.com/2021/day/14

const _ = require('underscore');
const fs = require('fs');
const { values } = require('underscore');

const FILE = '2021/d14/input';

const raw_data = fs.readFileSync(FILE, 'utf8');
[template, rules] = raw_data.split('\n\n');

// Better version for problem 2. Now we don't keep a template string anymore,
// we just track how many of each pair of letters are in the template lest
// we succumb to combninatoral explosion. Now,
//
// ruleMap = { 'XY' : ['XZ', 'ZX'], ...}
ruleMap = {}
_.each(rules.split('\n'), (r) => ruleMap[r.substring(0, 2)] = [r[0] + r[6], r[6] + r[1]]);

// Load up the inital population from the template string
// population = { 'XX': number, ... }
population = {}
_.each(_.range(template.length - 1), (i) => {
  key = template.substring(i, i + 2);
  key in population ? population[key]++ : population[key] = 1;
});

// At each step we know if there are N XY pairs and the XY rule is
// 'XY -> Z', then we need to add N to both XZ and ZY in the next
// generation. Note we don't need to keep any XY, but they'll
// be created elsewhere.
function step(ruleMap, population) {
  ret = {}
  _.each(population, (v, k) => {
    _.each(ruleMap[k], (t) => {
      t in ret ? ret[t] += v : ret[t] = v;
    })
  });
  return ret;
}

population = _.range(40).reduce((a, b) => step(ruleMap, a), population);

// count letter frequency for each pair
freq = {}
_.each(population, (v,k) => {
  _.each(k, (i) => {
    i in freq ? freq[i] += v : freq[i] = v;
  })
});

// A little accounting since everything is double counted except the first and last
freq[template[0]] += 1;
freq[template[template.length-1]] += 1;

// divide by 2 and print max-min
_.each(_.keys(freq), (k) => freq[k] /= 2);
console.log(Math.max(..._.values(freq)) - Math.min(..._.values(freq)));

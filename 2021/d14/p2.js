const _ = require('underscore');
const fs = require('fs');
const { values } = require('underscore');

const FILE = '2021/d14/input';

const raw_data = fs.readFileSync(FILE, 'utf8');
[tmplt, rules] = raw_data.split('\n\n');

ruleMap = {}
_.each(rules.split('\n'), (r) => ruleMap[r.substring(0, 2)] = [r[0] + r[6], r[6] + r[1]]);

population = {}
_.each(_.range(tmplt.length - 1), (i) => {
  key = tmplt.substring(i, i + 2);
  key in population ? population[key]++ : population[key] = 1;
});

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

freq = {}
_.each(population, (v,k) => {
  _.each(k, (i) => {
    i in freq ? freq[i] += v : freq[i] = v;
  })
});

// A little accounting since everything is double counted except the first and last
freq[tmplt[0]] += 1;
freq[tmplt[tmplt.length-1]] += 1;
_.each(_.keys(freq), (k) => freq[k] /= 2);

console.log(Math.max(..._.values(freq)) - Math.min(..._.values(freq)));

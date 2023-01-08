// https://adventofcode.com/day/14

const _ = require('underscore');
const fs = require('fs');

const FILE = 'd14/input';

const raw_data = fs.readFileSync(FILE, 'utf8');
[template, rules] = raw_data.split('\n\n');

// ruleMap = { 'XY': 'Z', ... }, where XX gets translated to XYZ in the template string
ruleMap = {}
_.each(rules.split('\n'), (r) => ruleMap[r.substring(0,2)] = r[6]);

// Build a new template string at each step, which is just the
// old template with the new letters inbetween.
function step(ruleMap, template) {
  let result = '';
  for (let i = 0; i < template.length-1; i++) {
    result += template[i];
    key = template.substring(i, i+2);
    result += key in ruleMap ? ruleMap[key] : '';
  }
  result += template[template.length-1];
  return result;
}

template = _.range(10).reduce((a, b) => step(ruleMap, a), template);

// count letter frequency in the final template and print max-min
counts = _.values(_.countBy(template));
console.log(Math.max(...counts) - Math.min(...counts));
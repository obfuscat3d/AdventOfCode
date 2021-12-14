const _ = require('underscore');
const fs = require('fs');

const FILE = 'd14/input2';

const raw_data = fs.readFileSync(FILE, 'utf8');
[tmplt, rules] = raw_data.split('\n\n');

ruleMap = {}
_.each(rules.split('\n'), (r) => ruleMap[r.substring(0,2)] = r[6]);

function step(ruleMap, tmplt) {
  let result = '';
  for (let i = 0; i < tmplt.length-1; i++) {
    result += tmplt[i];
    key = tmplt.substring(i, i+2);
    result += key in ruleMap ? ruleMap[key] : '';
  }
  result += tmplt[tmplt.length-1];
  return result;
}

for (let i = 0; i < 40; i++) {
  console.log(i);
  tmplt = step(ruleMap, tmplt);
}

counts = _.values(_.countBy(tmplt));
console.log(Math.max(...counts) - Math.min(...counts));
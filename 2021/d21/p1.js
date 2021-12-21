const _ = require('underscore');

const die = { rolls: 0, value: 99 };
function roll() {
  die.rolls++;
  return (die.value = ++die.value % 100) + 1;
}

// Location from input, corresponds to positions 10 and 7
player_pos = [9, 6]
player_turn = 0
player_score = [0, 0]

while (!_.find(player_score, x => x >= 1000)) {
  player_pos[player_turn] += roll() + roll() + roll();
  player_pos[player_turn] %= 10;
  player_score[player_turn] += player_pos[player_turn] + 1;
  player_turn = (player_turn + 1) % 2
}

console.log(die.rolls * _.min(player_score));
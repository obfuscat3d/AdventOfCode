const _ = require('underscore');

// Universe = pos1, pos2, score1, score2, turn
initial_universe = [9, 6, 0, 0, 0] // correponds to positions 10 and 7

const universe_hash = (u) => u.join(',');
const GOAL = 21;

function do_single_roll(u, next_roll) {
  cur_player = u[4] < 3 ? 0 : 1; // index on current player for next two lines
  u[cur_player] = (u[cur_player] + next_roll) % 10; // update current player's position
  (u[4] % 3 == 2) && (u[2 + cur_player] = u[2 + cur_player] + u[cur_player] + 1); // only add to score if final roll in turn
  u[4] = (u[4] + 1) % 6 // increment turn, note the cache-friendly mod here
  return u; // return new universe
}

universe_cache = new Map(); // becasue cache, obvi
function play(u) {
  if (universe_cache.has(universe_hash(u))) { return universe_cache.get(universe_hash(u)); }
  if (u[2] >= GOAL) return [1, 0]; // player 1 wins
  if (u[3] >= GOAL) return [0, 1]; // player 2 wins

  // Universe branching here
  results = [
    play(do_single_roll(_.clone(u), 1)),
    play(do_single_roll(_.clone(u), 2)),
    play(do_single_roll(_.clone(u), 3))].reduce((a, b) => [a[0] + b[0], a[1] + b[1]], [0, 0])
  universe_cache.set(universe_hash(u), results);
  return results;
}

console.log(play(initial_universe));

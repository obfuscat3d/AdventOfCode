const _ = require('underscore');
const fs = require('fs');
const { MinPriorityQueue } = require('@datastructures-js/priority-queue');

WINNING_BOARD = '...........AAAABBBBCCCCDDDD';
MOVE_COST = {
  'A': 1,
  'B': 10,
  'C': 100,
  'D': 1000
};
HALLWAY = [0, 1, 3, 5, 7, 9, 10]
DOOR = {
  'A': 2,
  'B': 4,
  'C': 6,
  'D': 8
}
ROOM = {
  'A': [11, 12, 13, 14],
  'B': [15, 16, 17, 18],
  'C': [19, 20, 21, 22],
  'D': [23, 24, 25, 26]
}

const is_final = (b, c) => _.contains(ROOM[b[c]], c) && _.every(ROOM[b[c]], c0 => c0 < c || b[c0] == b[c]);
const hallway_clear = (b, x, y) => _.every(_.range(x, y).map(i => b[i] == '.'));

function hallway_moves(b, c) {
  if (!hallway_clear(b, DOOR[b[c]], c)) return [];
  room = ROOM[b[c]];

  target = -1;
  if (b[room[0]] != '.') return [];
  if (b[room[3]] == '.') target = room[3];
  if (b[room[2]] == '.' && b[room[3]] == b[c]) target = room[2];
  if (b[room[1]] == '.' && b[room[3]] == b[c] && b[room[2]] == b[c]) target = room[1];
  if (b[room[3]] == b[c] && b[room[2]] == b[c] && b[room[1]] == b[c]) target = room[0];
  if (target == -1) return [];

  distance = Math.abs(c - DOOR[b[c]]) + 1 + room.indexOf(target);
  nb = b.substr(0, target) + b[c] + b.substr(target + 1);
  nb = nb.substr(0, c) + '.' + nb.substr(c + 1);
  return { board: nb, cost: distance * MOVE_COST[b[c]] };
}

function room_moves(b, c) {
  room_index = Math.floor((c - 11) / 4); // to which room am I in?
  door = 2 + 2 * room_index; // what's the door to my current room?
  room_pos = (c - 11) % 4; // where am I in the room? 0 = top, 3 = bottom
  if (room_pos > 0 && b[c - 1] != '.') return [];
  targets = HALLWAY.filter(a => b[a] == '.');
  targets = targets.filter(t => hallway_clear(b, door, t));
  return targets.map(t => {
    distance = Math.abs(t - door) + 1 + room_pos;
    let nb = b.substr(0, t) + b[c] + b.substr(t + 1);
    nb = nb.substr(0, c) + '.' + nb.substr(c + 1);
    return { board: nb, cost: distance * MOVE_COST[b[c]] };
  });
}

function gen_moves(b, c) {
  if (b[c] == '.') return [];
  if (is_final(b, c)) return [];
  return c < 11 ? hallway_moves(b, c) : room_moves(b, c);
}

function djikstra(initial_board) {
  q = new MinPriorityQueue()
  q.enqueue({ board: initial_board, cost: 0 }, 0);
  seen = new Set();

  while (q.size()) {
    cur = q.dequeue();
    [board, cost] = [cur.element.board, cur.element.cost];
    if (!seen.has(board)) {
      seen.add(board);

      if (board == WINNING_BOARD) {
        return cost;
      } else {
        new_moves = _.flatten(_.range(27).map(c => gen_moves(board, c)), 1);
        _.each(new_moves, move =>
          seen.has(move.board) || q.enqueue({ board: move.board, cost: cost + move.cost }, cost + move.cost));
      }
    }
  }
  return -1;
}

INITIAL_BOARD = '...........ADDCDCBCABADBACB';
console.log(djikstra(INITIAL_BOARD));

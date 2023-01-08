// https://adventofcode.com/day/4

const _ = require('underscore');
const fs = require('fs');

const FILE = 'd4/input';
const raw_data = fs.readFileSync(FILE, 'utf8');

class BingoBoard {
  constructor(text_board) {
    this.winners = _.range(10).map((i) => Array());
    this.numbers = [];
    this.parseBoard(text_board);
  }

  // We don't need to care about actually keeping a 5x5 board around,
  // just sets of winning numbers and sets of numbers not yet seen.
  parseBoard(text_board) {
    this.numbers = text_board.trim().split(/\s+/s).map(Number);
    for (let i in this.numbers) {
      this.winners[5 + i % 5].push(this.numbers[i]);
      this.winners[Math.floor(i / 5)].push(this.numbers[i]);
    }
  }

  go(num) {
    this.numbers = this.numbers.filter((n) => n != num);
    this.winners = this.winners.map((w) => w.filter((n) => n != num));

    if (_.some(this.winners, (n) => n.length == 0)) {
      console.log('winner! ' + num);
      console.log(num * this.numbers.reduce((a, b) => a + b, 0));
      process.exit(); // terminate after the first winner
    }
  }
}

numbers = raw_data.split('\n')[0].split(',').map((n) => parseInt(n));
text_boards = _.rest(raw_data.split(/\n\n/));
boards = text_boards.map((t) => new BingoBoard(t));

// For each number, iterate over the boards calling go(num)
// The answer is whatever board finishes first
_.each(numbers, (n) => _.each(boards, (b) => b.go(n)));


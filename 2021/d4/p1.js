// https://adventofcode.com/2021/day/4

const _ = require('underscore');
const fs = require('fs');

const FILE = '2021/d4/input';
const raw_data = fs.readFileSync(FILE, 'utf8');

class BingoBoard {
  constructor(text_board) {
    this.winners = _.range(10).map((i) => Array());
    this.numbers = [];
    this.parseBoard(text_board);
  }

  parseBoard(text_board) {
    this.numbers = text_board.trim().split(/\s+/s).map((n) => parseInt(n));
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
      console.log(num * this.numbers.reduce((a,b) => a+b, 0));
      process.exit();
    }
  }
}

numbers = raw_data.split('\n')[0].split(',').map((n) => parseInt(n));
text_boards = _.rest(raw_data.split(/\n\n/));
boards = text_boards.map((t) => new BingoBoard(t));

for (let i in numbers) {
  _.each(boards, (b) => b.go(numbers[i]));
}

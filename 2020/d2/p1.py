import re

FILE = '2020/d2/input'

# returns a tuple (letter, num, num, password)
def parse(line):
  remainder, pw = line.split(': ')
  remainder, letter = remainder.split(' ')
  min, max = remainder.split('-')
  return (letter, int(min), int(max), pw)

def check1(letter, min, max, pw):
  return min <= pw.count(letter) <= max

def part1(data):
  print(len([x for x in data if check1(x[0], x[1], x[2], x[3])]))

def check2(letter, pos1, pos2, pw):
  return (pw[pos1-1] == letter) ^ (pw[pos2-1] == letter)

def part2(data):
  print(len([x for x in data if check2(x[0], x[1], x[2], x[3])]))

if __name__ == '__main__':
  with open(FILE) as input:
    data = [parse(line) for line in input.read().splitlines()]

  part1(data)
  part2(data)
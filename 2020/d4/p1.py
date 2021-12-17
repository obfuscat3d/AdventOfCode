import numpy as np
from pprint import *
import re

FILE = '2020/d4/input'


def byr(x): return 1920 <= int(x) <= 2002
def iyr(x): return 2010 <= int(x) <= 2020
def eyr(x): return 2020 <= int(x) <= 2030
def ecl(x): return x in 'amb blu brn gry grn hzl oth'.split(' ')
def hcl(x): return re.match(r"^#[0-9a-f]{6}$", x)
def pid(x): return re.match(r"^[\d]{9}$", x)


def hgt(x):
  [lo, hi] = [150, 193] if x.find('cm') != -1 else [59, 76]
  ret = lo <= int(re.findall(r"[\d]{2,3}", x)[0]) <= hi
  return ret


REQUIRED = {'byr': byr,
      'iyr': iyr,
      'eyr': eyr,
      'hgt': hgt,
      'hcl': hcl,
      'ecl': ecl,
      # 'cid', # this is always ignored
      'pid': pid}


def is_valid(p, check_data=False):
  for field in REQUIRED.keys():
    if field not in p:
      return False
    if check_data and not REQUIRED[field](p[field]):
      return False
  return True


with open(FILE) as input:
  raw_data = input.read().split('\n\n')
  passports = [
    {s[:s.index(':')]:s[s.index(':')+1:]
     for s in pp.replace('\n', ' ').split(' ')}
    for pp in raw_data]


# Part 1
#pprint(len([1 for p in passports if is_valid(p)]))

# Part 2
pprint(len([1 for p in passports if is_valid(p, True)]))

# 134 too high

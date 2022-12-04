from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

item_values = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'f': 6,
    'g': 7,
    'h': 8,
    'i': 9,
    'j': 10,
    'k': 11,
    'l': 12,
    'm': 13,
    'n': 14,
    'o': 15,
    'p': 16,
    'q': 17,
    'r': 18,
    's': 19,
    't': 20,
    'u': 21,
    'v': 22,
    'w': 23,
    'x': 24,
    'y': 25,
    'z': 26,
}

def chunk_list(l: list, n: int) -> list:
    for i in range(0, len(l), n):
        yield l[i: i + n]

def compute(s: str) -> int:
    l = s.split('\n')

    grp_3 = chunk_list(l, 3)

    item_totals = 0
    for g in grp_3:
        for itm in set(g[0]):
            if (itm in g[1]) & (itm in g[2]):
                item_totals += item_values.get(itm.lower())
                if itm == itm.upper():
                    item_totals += 26
                continue
    return item_totals


def part1(s: str) -> int:
    l = s.split('\n')

    item_totals = 0
    for i in l:
        if len(i) == 0:
            continue

        rs_middle = int(len(i)/2)
        item_1 = i[0:rs_middle]
        item_2 = i[rs_middle:]
        for itm in set(list(item_1)):
            if itm in item_2:
                item_totals += item_values.get(itm.lower())
                if itm == itm.upper():
                    item_totals += 26
                continue
    return item_totals


INPUT_S = '''\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''
EXPECTED = 157

EXPECTED_P2 = 70

@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # (INPUT_S, EXPECTED),
        (INPUT_S, EXPECTED_P2),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

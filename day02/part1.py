from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def rps(c: str, o: str) -> int:
	if c == o:
	    return 3
	elif c == 'rock':
	    if o == 'paper':
	        return 0
	    elif o == 'scissors':
	        return 6
	elif c == 'paper':
	    if o == 'rock':
	        return 6
	    elif o == 'scissors':
	        return 0
	elif c == 'scissors':
	    if o == 'rock':
	        return 0
	    elif o == 'paper':
	        return 6

def rps_strat(c_strat: str, o: str) -> str:
    if c_strat == 'X':
        #lose
        if o == 'rock':
            return 'scissors'
        if o == 'paper':
            return 'rock'
        if o == 'scissors':
            return 'paper'
    elif c_strat == 'Y':
        #draw
        return o
    elif c_strat == 'Z':
        #win
        if o == 'rock':
            return 'paper'
        if o == 'paper':
            return 'scissors'
        if o == 'scissors':
            return 'rock'

def compute(s: str) -> int:
    guide_cnv = {
        'A': 'rock',
        'B': 'paper',
        'C': 'scissors',
        'X': 'rock',
        'Y': 'paper',
        'Z': 'scissors',
    }

    attack_pts = {
        'rock': 1,
        'paper': 2,
        'scissors': 3,
    }

    raw_inputs = s.split('\n')
    inputs = []
    for r in raw_inputs:
        tmp = r.split(' ')
        if len(tmp) != 2:
            continue
        else:
            inputs.append(tmp)

    pts_total = 0
    for i in inputs:
        #contestant = guide_cnv.get(i[1])
        opp = guide_cnv.get(i[0])
        contestant = rps_strat(i[1], opp)

        pts_total += attack_pts[contestant]
        pts_total += rps(contestant, opp)

    return pts_total


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 15

TWIST_I = '''\
A Y
B X
C Z
'''
TWIST_E = 12

@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        #(INPUT_S, EXPECTED),
        (TWIST_I, TWIST_E),
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

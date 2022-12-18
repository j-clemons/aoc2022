from __future__ import annotations

import argparse
import os.path

import pytest

import support

import re

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def mahattan_dist(a: tuple, b: tuple) -> int: 
    ax, ay = a
    bx, by = b

    return abs(ax - bx) + abs(ay - by)

def compute(s: str) -> int:
    lines = s.splitlines()
    coverage = []
    for line in lines:
        # parse sensor / beacon data
        sensor, beacon = line.split(':')
        sx = int(re.search('(?:x=)[-0-9]*', sensor).group().replace('x=',''))
        sy = int(re.search('(?:y=)[-0-9]*', sensor).group().replace('y=',''))
        bx = int(re.search('(?:x=)[-0-9]*', beacon).group().replace('x=',''))
        by = int(re.search('(?:y=)[-0-9]*', beacon).group().replace('y=',''))
        # determine distance from sensor to beacon
        dist = abs(sx - bx) + abs(sy - by)
        
        # create diamond of locations that cannot contain a beacon. Add to list
        top = sy - dist
        bottom = sy + dist

        # set row number target
        target_row = 2000000
        for i in range(top, bottom + 1):
            if i == target_row:
                remain = dist - abs(sy - i)
                if (remain == 0) & ((sx, i) != (bx, by)): 
                    coverage.append((sx, i))
                else:
                    lft = (sx - remain)
                    rgt = (sx + remain)

                    for j in range(lft, rgt + 1):
                        if (j, i) != (bx, by):
                            coverage.append((j, i))

    return len(set(coverage))


INPUT_S2 = '''\
Sensor at x=8, y=7: closest beacon is at x=2, y=10
'''
INPUT_S = '''\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''
EXPECTED = 26


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
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

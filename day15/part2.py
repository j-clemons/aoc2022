from __future__ import annotations

import argparse
import os.path

import pytest

import support

import re
from z3 import If
from z3 import Int
from z3 import Optimize
from z3 import Solver
from z3 import sat

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def z3_abs(expr):
    return If(expr > 0, expr, -expr)

def compute(s: str) -> int:
    m = 4000000

    o = Solver() # Optimize()
    X = Int('X')
    Y = Int('Y')
    o.add(0 <= X)
    o.add(0 <= Y)
    o.add(X <= m)
    o.add(Y <= m)

    lines = s.splitlines()

    for line in lines:
        # parse sensor / beacon data
        sensor, beacon = line.split(':')
        sx = int(re.search('(?:x=)[-0-9]*', sensor).group().replace('x=',''))
        sy = int(re.search('(?:y=)[-0-9]*', sensor).group().replace('y=',''))
        bx = int(re.search('(?:x=)[-0-9]*', beacon).group().replace('x=',''))
        by = int(re.search('(?:y=)[-0-9]*', beacon).group().replace('y=',''))

        # determine distance from sensor to beacon
        dist = abs(sx - bx) + abs(sy - by)

        o.add((z3_abs(sx - X) + z3_abs(sy - Y)) > dist)

    assert o.check() == sat
    result = o.model()

    return print((result[X].as_long() * 4000000) + result[Y].as_long())


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
EXPECTED = 56000011

aoc_input = '''\
Sensor at x=2692921, y=2988627: closest beacon is at x=2453611, y=3029623
Sensor at x=1557973, y=1620482: closest beacon is at x=1908435, y=2403457
Sensor at x=278431, y=3878878: closest beacon is at x=-1050422, y=3218536
Sensor at x=1432037, y=3317707: closest beacon is at x=2453611, y=3029623
Sensor at x=3191434, y=3564121: closest beacon is at x=3420256, y=2939344
Sensor at x=3080887, y=2781756: closest beacon is at x=3420256, y=2939344
Sensor at x=3543287, y=3060807: closest beacon is at x=3420256, y=2939344
Sensor at x=2476158, y=3949016: closest beacon is at x=2453611, y=3029623
Sensor at x=3999769, y=3985671: closest beacon is at x=3420256, y=2939344
Sensor at x=2435331, y=2200565: closest beacon is at x=1908435, y=2403457
Sensor at x=3970047, y=2036397: closest beacon is at x=3691788, y=1874066
Sensor at x=2232167, y=2750817: closest beacon is at x=2453611, y=3029623
Sensor at x=157988, y=333826: closest beacon is at x=-1236383, y=477990
Sensor at x=1035254, y=2261267: closest beacon is at x=1908435, y=2403457
Sensor at x=1154009, y=888885: closest beacon is at x=1070922, y=-543463
Sensor at x=2704724, y=257848: closest beacon is at x=3428489, y=-741777
Sensor at x=3672526, y=2651153: closest beacon is at x=3420256, y=2939344
Sensor at x=2030614, y=2603134: closest beacon is at x=1908435, y=2403457
Sensor at x=2550448, y=2781018: closest beacon is at x=2453611, y=3029623
Sensor at x=3162759, y=2196461: closest beacon is at x=3691788, y=1874066
Sensor at x=463834, y=1709480: closest beacon is at x=-208427, y=2000000
Sensor at x=217427, y=2725325: closest beacon is at x=-208427, y=2000000
Sensor at x=3903198, y=945190: closest beacon is at x=3691788, y=1874066
'''

@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    # parser = argparse.ArgumentParser()
    # parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    # args = parser.parse_args()
    #
    # with open(args.data_file) as f, support.timing():
    #     print(compute(f.read()))
    compute(aoc_input)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

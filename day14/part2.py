from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def add_tuple(t1: tuple, t2: tuple) -> tuple:

    return tuple(map(sum, zip(t1, t2)))


def compute(s: str) -> int:
    pts = set()
    lines = s.splitlines()
    for line in lines:
        inputs = line.split(' -> ')
        path = [x.split(',') for x in inputs]
        prev = (-1, -1)
        for p in range(0, len(path)):
            if p == 0:
                pr_x, pr_y = [int(x) for x in path[p]]
            else:
                x, y = [int(x) for x in path[p]]

                if (pr_x > x) & (pr_y == y):
                    pts.update({(i, y) for i in range(x, pr_x + 1)})
                
                elif (pr_x < x) & (pr_y == y):
                    pts.update({(i, y) for i in range(pr_x, x + 1)})

                elif (pr_x == x) & (pr_y > y):
                    pts.update({(x, i) for i in range(y, pr_y + 1)})

                elif (pr_x == x) & (pr_y < y):
                    pts.update({(x, i) for i in range(pr_y, y + 1)})

                pr_x = x
                pr_y = y

    floor = max([f[1] for f in pts]) + 2
    pts.update({(f, floor) for f in range(500-floor-2, 500+floor+2)})

    sand = set()
    sand_start = (500, 0)
    total_add = True
    while total_add:
        tmp = sand_start
        attempt_add = True
        while attempt_add:
            dwn = add_tuple(tmp, (0,1))
            lft = add_tuple(tmp, (-1, 1))
            rgt = add_tuple(tmp, (1, 1))
            if (dwn in pts) & (lft in pts) & (rgt in pts):
                pts.add(tmp)
                sand.add(tmp)
                attempt_add = False
                if tmp == sand_start:
                    total_add = False

            elif (dwn in pts) & (lft not in pts):
                tmp = add_tuple(dwn, (-1,0))
                continue

            elif (dwn in pts) & (lft in pts) & (rgt not in pts):
                tmp = add_tuple(dwn, (1,0))
                continue
            else:
                tmp = dwn

    return len(sand) 


INPUT_S = '''\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
EXPECTED = 93


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

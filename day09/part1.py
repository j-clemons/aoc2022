from __future__ import annotations

import argparse
import os.path

import pytest

import support

import operator

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def add_tuple(t1: tuple, t2: tuple) -> tuple:

    return tuple(map(sum, zip(t1, t2)))

def dist(t1: tuple, t2: tuple) -> int:

    return round(((t1[0] - t2[0])**2 + (t1[1] - t2[1])**2)**(1/2), 2)

def part1(s: str) -> int:
    h = (0, 0)
    t = (0, 0)

    positions = [t]

    move = {
        'R': (1, 0),
        'L': (-1, 0),
        'U': (0, 1),
        'D': (0, -1),
    }

    lines = s.splitlines()
    for line in lines:
        l = line.split(' ')
        dir = l[0]
        mv = move.get(dir)
        for i in range(0, int(l[1])):
            tmp = h
            h = add_tuple(tmp, mv)

            if dist(h, t) <= 1.41:
                pass
            else:
                if dir == 'R':
                    t = add_tuple(h, (-1, 0))
                elif dir == 'L':
                    t = add_tuple(h, (1, 0))
                elif dir == 'U':
                    t = add_tuple(h, (0, -1))
                elif dir == 'D':
                    t = add_tuple(h, (0, 1))

                positions.append(t)

    return len(set(positions))


def move_tail(lead: tuple, tail: tuple) -> tuple:
    l1, l2 = lead
    t1, t2 = tail

    if (abs(l1 - t1) == 2) & (abs(l2 - t2) == 2):
        return ((l1 + t1) // 2, (l2 + t2) // 2)
    if abs(l1 - t1) == 2:
        return ((l1 + t1) // 2, l2)
    elif abs(l2 - t2) == 2:
        return (l1, (l2 + t2) // 2)
    else:
        return tail


def compute(s: str) -> int:
    rope = [
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
    ]
    positions = [rope[0]]

    move = {
        'R': (1, 0),
        'L': (-1, 0),
        'U': (0, 1),
        'D': (0, -1),
    }

    lines = s.splitlines()
    for line in lines:
        l = line.split(' ')
        dir = l[0]

        # loop for number of moves of the head
        for i in range(0, int(l[1])):

            pp = rope[0]
            # get the initial move
            mv = move.get(dir)
            # loop through each knot. Exclude last knot.
            for k in range(0, len(rope)):
                l = rope[k]

                if k == 0:
                    # move the leader
                    tmp = l
                    l = add_tuple(tmp, mv)
                    rope[k] = l

                else:
                    rope[k] = move_tail(pp, rope[k])

                pp = rope[k]

                positions.append(rope[9])

    return len(set(positions))


INPUT_S = '''\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''
EXPECTED = 13

INPUT_P2 = '''\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''
EXPECTED_P2 = 36

@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
#        (INPUT_S, EXPECTED),
        (INPUT_P2, EXPECTED_P2),
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

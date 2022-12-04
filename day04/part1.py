from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    overlap_count = 0

    for line in lines:
        pairs = line.split(',')
        p1 = [int(x) for x in pairs[0].split('-')]
        p2 = [int(x) for x in pairs[1].split('-')]

        if ((p1[0] >= p2[0]) & (p1[0] <= p2[1])) \
            | ((p1[1] >= p2[0]) & (p1[1] <= p2[1])) \
            | ((p2[0] >= p1[0]) & (p2[0] <= p1[1])) \
            | ((p2[1] >= p1[0]) & (p2[1] <= p1[1])):
            overlap_count += 1
        else:
            continue
    return overlap_count


def fully_contains_match(s: str) -> int:
    lines = s.splitlines()
    full_match_count = 0

    for line in lines:
        pairs = line.split(',')
        p1 = [int(x) for x in pairs[0].split('-')]
        p2 = [int(x) for x in pairs[1].split('-')]

        if (p1[0] <= p2[0]) & (p1[1] >= p2[1]):
            full_match_count += 1
        elif (p2[0] <= p1[0]) & (p2[1] >= p1[1]):
            full_match_count += 1
        else:
            continue
    return full_match_count


INPUT_S = '''\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''
EXPECTED = 2

P2_EXPECTED = 4


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # (INPUT_S, EXPECTED),
        (INPUT_S, P2_EXPECTED),
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

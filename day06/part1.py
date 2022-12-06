from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    chars = list(s)
    marker_len = 14

    for i in range(marker_len, len(chars)+1):
        tmp = set(chars[i-marker_len:i])
        if len(tmp) == marker_len:
            return i

    return 0


INPUT_S = '''\
mjqjpqmgbljsphdztnvjfqwrcgsmlb
'''
EXPECTED = 7

INPUT_2 = '''\
bvwbjplbgvbhsrlpgdmjqwftvncz
'''
EXPECTED_2 = 5

INPUT_3 = '''\
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
'''
EXPECTED_3 = 10

@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
        (INPUT_2, EXPECTED_2),
        (INPUT_3, EXPECTED_3),
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

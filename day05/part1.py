from __future__ import annotations

from collections import deque

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# [B]                     [N]     [H]
# [V]         [P] [T]     [V]     [P]
# [W]     [C] [T] [S]     [H]     [N]
# [T]     [J] [Z] [M] [N] [F]     [L]
# [Q]     [W] [N] [J] [T] [Q] [R] [B]
# [N] [B] [Q] [R] [V] [F] [D] [F] [M]
# [H] [W] [S] [J] [P] [W] [L] [P] [S]
# [D] [D] [T] [F] [G] [B] [B] [H] [Z]
#  1   2   3   4   5   6   7   8   9

# part 2
def compute(s: str) -> str:
    s1 = deque(['D', 'H', 'N', 'Q', 'T', 'W', 'V', 'B'])
    s2 = deque(['D', 'W', 'B'])
    s3 = deque(['T', 'S', 'Q', 'W', 'J', 'C'])
    s4 = deque(['F', 'J', 'R', 'N', 'Z', 'T', 'P'])
    s5 = deque(['G', 'P', 'V', 'J', 'M', 'S', 'T'])
    s6 = deque(['B', 'W', 'F', 'T', 'N'])
    s7 = deque(['B', 'L', 'D', 'Q', 'F', 'H', 'V', 'N'])
    s8 = deque(['H', 'P', 'F', 'R'])
    s9 = deque(['Z', 'S', 'M', 'B', 'L', 'N', 'P', 'H'])

    stack_ref = {
        1: s1,
        2: s2,
        3: s3,
        4: s4,
        5: s5,
        6: s6,
        7: s7,
        8: s8,
        9: s9,
    }

    tmp = deque()
    lines = s.splitlines()
    for line in lines:
        nums = [int(x) for x in line.split(' ') if x.isdigit()]

        for _ in range(0, nums[0]):
            tmp.append(stack_ref.get(nums[1]).pop())

        for _ in range(0, nums[0]):
            stack_ref.get(nums[2]).append(tmp.pop())

    return (s1.pop() + s2.pop() + s3.pop() + s4.pop() + s5.pop() + s6.pop() + s7.pop() + s8.pop() + s9.pop()).strip()

# part 1
def cm9000(s: str) -> str:
    s1 = deque(['D', 'H', 'N', 'Q', 'T', 'W', 'V', 'B'])
    s2 = deque(['D', 'W', 'B'])
    s3 = deque(['T', 'S', 'Q', 'W', 'J', 'C'])
    s4 = deque(['F', 'J', 'R', 'N', 'Z', 'T', 'P'])
    s5 = deque(['G', 'P', 'V', 'J', 'M', 'S', 'T'])
    s6 = deque(['B', 'W', 'F', 'T', 'N'])
    s7 = deque(['B', 'L', 'D', 'Q', 'F', 'H', 'V', 'N'])
    s8 = deque(['H', 'P', 'F', 'R'])
    s9 = deque(['Z', 'S', 'M', 'B', 'L', 'N', 'P', 'H'])

    stack_ref = {
        1: s1,
        2: s2,
        3: s3,
        4: s4,
        5: s5,
        6: s6,
        7: s7,
        8: s8,
        9: s9,
    }

    lines = s.splitlines()
    for line in lines:
        nums = [int(x) for x in line.split(' ') if x.isdigit()]

        for _ in range(0, nums[0]):
            stack_ref.get(nums[2]).append(stack_ref.get(nums[1]).pop())

    return (s1.pop() + s2.pop() + s3.pop() + s4.pop() + s5.pop() + s6.pop() + s7.pop() + s8.pop() + s9.pop()).rstrip()


INPUT_S = '''\
move 2 from 8 to 1
move 4 from 9 to 8
move 2 from 1 to 6
'''
EXPECTED = 'BBCPTRNLB'

P2_EXPECTED = 'BBCPTRNHB'

@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # (INPUT_S, EXPECTED),
        (INPUT_S, P2_EXPECTED),
    ),
)
def test(input_s: str, expected: str) -> None:
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

from __future__ import annotations

import argparse
import os.path

import pytest

import support

import numpy as np

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def visible_from_outside(s: str) -> int:
    lines = s.splitlines()
    height = len(lines)
    width = len([x for x in list(lines[0])])

    arr = np.eye(height, width)
    res_arr = np.eye(height, width)
    itr = 0
    for line in lines:
        arr[itr]= np.array([int(x) for x in list(line)])
        itr += 1

    # Iterate through each row
    for r in range(0, height):
        # Iterate through each column
        for c in range(0, width):
            if (r == 0) | (r == height - 1) | (c == 0) | (c == width - 1):
                res_arr[r, c] = 1
            else:
                val = arr[r, c]
                lft = max(arr[r, :c])
                rgt = max(arr[r, c+1:])
                up  = max(arr[:r, c])
                dwn = max(arr[r+1:, c])

                if (val > lft) | (val > rgt) | (val > up) | (val > dwn):
                    res_arr[r, c] = 1
                else:
                    res_arr[r, c] = 0

    return int(res_arr.sum())

def visible_distance(l: list, tree_height: int) -> int:
    dist = 0
    if l[0] == 0:
        return 0

    for i in l:
        if i >= tree_height:
            dist += 1
            break
        elif i < tree_height:
            dist += 1

    return dist

def scenic_score(s: str) -> int:
    lines = s.splitlines()
    height = len(lines)
    width = len([x for x in list(lines[0])])

    arr = np.eye(height, width)
    res_arr = np.eye(height, width)
    itr = 0
    for line in lines:
        arr[itr]= np.array([int(x) for x in list(line)])
        itr += 1

    # Iterate through each row
    for r in range(0, height):
        # Iterate through each column
        for c in range(0, width):
            val = int(arr[r, c])
            up = [0] if r == 0 else list(arr[:r, c])
            up.reverse()

            dwn = [0] if r == (height - 1) else list(arr[r+1:, c])

            lft = [0] if c == 0 else list(arr[r, :c])
            lft.reverse()

            rgt = [0] if c == (width - 1) else list(arr[r, c+1:])

            score = visible_distance(up, val) \
                * visible_distance(dwn, val) \
                * visible_distance(lft, val) \
                * visible_distance(rgt, val)

            res_arr[r, c] = score

    return int(res_arr.max())

INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 21

EXPECTED_SS = 9

@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # (INPUT_S, EXPECTED),
        (INPUT_S, EXPECTED_SS),
    ),
)
def test(input_s: str, expected: int) -> None:
    # assert visible_from_outside(input_s) == expected
    assert scenic_score(input_s) == expected

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(scenic_score(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

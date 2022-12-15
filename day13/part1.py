from __future__ import annotations

import argparse
import os.path

import pytest

import support

import ast

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def comp_list(l1: list, l2: list) -> boolean:
    for i in range(0, len(l1)):
        tl1 = l1[i]

        try:
            tl2 = l2[i]
        except IndexError:
            return False

        tl1_type = type(tl1)
        tl2_type = type(tl2)

        if (tl1 == []) & (tl2 == []):
            continue

        if (tl1_type == int) & (tl2_type == int):
            if tl1 < tl2:
                return True
            elif tl1 > tl2:
                return False
            else:
                continue
        elif (tl1_type == list) & (tl2_type == list):
            return comp_list(tl1, tl2)

        elif (tl1_type == list) & (tl2_type == int):
            return comp_list(tl1, [tl2])

        elif (tl1_type == int) & (tl2_type == list):
            return comp_list([tl1], tl2)

    return True

def list_unpack(nl: list) -> list:
    if len(nl) == 1:
        if type(nl[0]) == list:
            return list_unpack(nl[0])
        else:
            return nl

    return nl

def debug_comp_list(l1: list, l2: list) -> boolean:
    for i in range(0, len(l1)+1):
#        if (l1 == []) & (l2 == []):
#            continue

        try:
            tl1 = l1[i]
        except IndexError:
            return True
        try:
            tl2 = l2[i]
        except IndexError:
            return False

        tl1_type = type(tl1)
        tl2_type = type(tl2)

        print(tl1_type, tl1)
        print(tl2_type, tl2)

        if (tl1 == []) & (tl2 == []):
            continue

        if (tl1_type == int) & (tl2_type == int):
            if tl1 < tl2:
                return True
            elif tl1 > tl2:
                return False
            else:
                return comp_list(l1[i+1], l2[i+1])
        elif (tl1_type == list) & (tl2_type == list):
            return comp_list(list_unpack(tl1), list_unpack(tl2))

        elif (tl1_type == list) & (tl2_type == int):
            return comp_list(list_unpack(tl1), [tl2])

        elif (tl1_type == int) & (tl2_type == list):
            return comp_list([tl1], list_unpack(tl2))

    return False



def compute(s: str) -> int:
    itr = 1
    c1 = []
    c2 = []
    correct_pairs = []

    test_pairs = []
    lines = s.splitlines()
    for line in range(0, len(lines)):
        if line % 3 == 0:
            c1 = ast.literal_eval(lines[line])
        elif line % 3 == 1:
            c2 = ast.literal_eval(lines[line])
            test_pairs.append([c1, c2])
#        elif line % 3 == 2:
#            # compare c1 & c2.
#            # If correct append to correct_pairs.
#            # update itr
#            if comp_list(c1, c2) == True:
#                correct_pairs.append(itr)

#            itr += 1

    for p in range(0, len(test_pairs)):
        if comp_list(test_pairs[p][0], test_pairs[p][1]) == True:
            correct_pairs.append(p+1)

    breakpoint()
    return sum(correct_pairs)


INPUT_S = '''\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''
EXPECTED = 13


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

from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    l = s.split('\n')

    r = []
    c = 0
    for i in l:
        if i == '':
            r.append(int(c))
            c = 0
        else:
            c += int(i)

    r.sort(reverse=True)

    # TODO: implement solution here!
    return sum(r[:3])


INPUT_S = '''\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
'''
EXPECTED = 24000

INPUT_2 = '''\
9548
3738

18492
17104
1738
'''
EXPECTED_2 = 37334

INPUT_3 = '''\
9548
3738

45000

18492
17104
1738
'''
EXPECTED_3 = 45000

INPUT_4 = '''\
1000
2000
3000

4000

5000
6000


7000
8000
9000


10000
'''
EXPECTED_4 = 24000

TWIST_1 = '''\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
'''
TW_EXPECTED_1 = 45000

@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # (INPUT_S, EXPECTED),
        # (INPUT_2, EXPECTED_2),
        # (INPUT_3, EXPECTED_3),
        # (INPUT_4, EXPECTED_4),
        (TWIST_1, TW_EXPECTED_1),
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

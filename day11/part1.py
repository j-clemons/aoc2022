from __future__ import annotations

import queue
from queue import Queue
from math import floor

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

class Monkey(object):
    def __init__(self, starting_items, test_input, test_true, test_false):
        self.items = Queue(maxsize = 0)
        for i in starting_items:
            self.items.put(i, timeout=1)

#        self.operation = operation
        self.test_input = test_input
        self.test_true = test_true
        self.test_false = test_false
        self.inspection_count = 0

    def test_item(self, value):
        if value % self.test_input == 0:
            return self.test_true
        else:
            return self.test_false

def compute(s: str) -> int:
    m0 = Monkey([72, 97], 19, 5, 6)
    m1 = Monkey([55, 70, 90, 74, 95], 7, 5, 0)
    m2 = Monkey([74, 97, 66, 57], 17, 1, 0)
    m3 = Monkey([86, 54, 53], 13, 1, 2)
    m4 = Monkey([50, 65, 78, 50, 62, 99], 11, 3, 7)
    m5 = Monkey([90], 2, 4, 6)
    m6 = Monkey([88, 92, 63, 94, 96, 82, 53, 53], 5, 4, 7)
    m7 = Monkey([70, 60, 71, 69, 77, 70, 98], 3, 2, 3)

    for _ in range(0, 20):

        for i in range(0, 8):

            while True:
                tmp = None
                dest = -1
                try:
                    if i == 0:
                        tmp = m0.items.get(timeout=1)
                        tmp = floor((tmp * 13) / 3)
                        m0.inspection_count += 1
                        dest = m0.test_item(tmp)
                    elif i == 1:
                        tmp = m1.items.get(timeout=1)
                        tmp = floor((tmp * tmp) / 3)
                        m1.inspection_count += 1
                        dest = m1.test_item(tmp)
                    elif i == 2:
                        tmp = m2.items.get(timeout=1)
                        tmp = floor((tmp + 6) / 3)
                        m2.inspection_count += 1
                        dest = m2.test_item(tmp)
                    elif i == 3:
                        tmp = m3.items.get(timeout=1)
                        tmp = floor((tmp + 2) / 3)
                        m3.inspection_count += 1
                        dest = m3.test_item(tmp)
                    elif i == 4:
                        tmp = m4.items.get(timeout=1)
                        tmp = floor((tmp + 3) / 3)
                        m4.inspection_count += 1
                        dest = m4.test_item(tmp)
                    elif i == 5:
                        tmp = m5.items.get(timeout=1)
                        tmp = floor((tmp + 4) / 3)
                        m5.inspection_count += 1
                        dest = m5.test_item(tmp)
                    elif i == 6:
                        tmp = m6.items.get(timeout=1)
                        tmp = floor((tmp + 8) / 3)
                        m6.inspection_count += 1
                        dest = m6.test_item(tmp)
                    elif i == 7:
                        tmp = m7.items.get(timeout=1)
                        tmp = floor((tmp * 7) / 3)
                        m7.inspection_count += 1
                        dest = m7.test_item(tmp)

                except queue.Empty:
                    break

                print(tmp, dest)

                if dest == 0:
                    m0.items.put(tmp, timeout=1)
                elif dest == 1:
                    m1.items.put(tmp, timeout=1)
                elif dest == 2:
                    m2.items.put(tmp, timeout=1)
                elif dest == 3:
                    m3.items.put(tmp, timeout=1)
                elif dest == 4:
                    m4.items.put(tmp, timeout=1)
                elif dest == 5:
                    m5.items.put(tmp, timeout=1)
                elif dest == 6:
                    m6.items.put(tmp, timeout=1)
                elif dest == 7:
                    m7.items.put(tmp, timeout=1)


    results = [
        m0.inspection_count,
        m1.inspection_count,
        m2.inspection_count,
        m3.inspection_count,
        m4.inspection_count,
        m5.inspection_count,
        m6.inspection_count,
        m7.inspection_count
    ]
    results.sort()
    results.reverse()

    return int(results[0] * results[1])


INPUT_S = '''\

'''
EXPECTED = 1


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

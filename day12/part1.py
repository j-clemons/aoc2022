from __future__ import annotations

import argparse
import os.path

import pytest

import support

import networkx as nx

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def get_moves(h_map: list, loc: tuple) -> list:
    map_height = len(h_map) - 1
    map_width = len(h_map[0]) - 1

    x, y = loc
    loc_elev = h_map[x][y]

    options = [
        (x-1, y),   # up
        (x+1, y),   # down
        (x, y-1),   # left
        (x, y+1),   # right
    ]

    results = []
    for o in options:
        ox, oy = o

        if (ox < 0) | (ox > map_height) | (oy < 0) | (oy > map_width):
            pass
        elif h_map[ox][oy] <= loc_elev + 1:
            results.append(o)

    return results

def compute(s: str) -> int:
    # Create numeric map, leaving start and end
    map = []
    lines = s.splitlines()
    for line in lines:
        num_list = [ord(x) - 96 if x not in ['S','E'] else x for x in list(line)]
        map.append(num_list)

    # get location of S and E
    s_loc = -1
    e_loc = -1
    for i in range(0, len(map)):
        try:
            s_ind = map[i].index('S')
            s_loc = (i * len(map[i])) + s_ind
            map[i][s_ind] = 0
        except ValueError:
            pass

        try:
            e_ind = map[i].index('E')
            e_loc = (i * len(map[i])) + e_ind
            map[i][e_ind] = 26
        except ValueError:
            pass

    g = nx.DiGraph()

    # create all graph nodes
    for r in range(0, len(map)):
        rl = len(map[r])
        for c in range(0, len(map[r])):
            g.add_node((r * rl) + c)

    # add all edges
    for r in range(0, len(map)):
        rl = len(map[r])
        for c in range(0, len(map[r])):
            moves = get_moves(map, (r, c))
            node = (r * rl) + c
            for mv in moves:
                x, y = mv
                g.add_edge(node, (x * rl) + y)

    return len(nx.shortest_path(g, s_loc, e_loc)) - 1


INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED = 31


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

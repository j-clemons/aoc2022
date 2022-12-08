from __future__ import annotations

from anytree import AnyNode, RenderTree, search

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    root = AnyNode(id='/', type='dir')
    dir = '/'
    
    current_depth = 0
    # Create a tree from the navigation instructions
    lines = s.splitlines()
    for line in lines:
        if line == '$ cd /':
            ln = root
            pass
        elif (line[:4] == '$ cd') & (line != '$ cd ..'):
            dir = line[4:].strip()
            parent = ln.parent
        elif line == '$ cd ..':
            try:
                tmp = search.find(
                    root,
                    lambda node: (node.id == dir) & (node.depth == current_depth - 1)).parent
                dir = tmp.id
                current_depth -= 1
            except:
                breakpoint()
                quit()
        elif line[:4] =='$ ls':
            pass
        else:
            dtl = line.split(' ')
            if dtl[0] == 'dir':
                ln = AnyNode(
                    id = dtl[1],
                    type = 'dir',
                    size = 0,
                    parent = search.find(root, lambda node: node.id == dir)
                )
            else:
                ln = AnyNode(
                    id = dtl[1],
                    type = 'file',
                    size = int(dtl[0]),
                    parent = search.find(root, lambda node: node.id == dir)
                )
            current_depth = ln.depth

    # iterate through tree to total sizes of each dir
    node_depth = root.height

    while node_depth > 0:
        avail_nodes = search.findall(root, lambda node: node.depth == node_depth)

        target_parents = {a.parent for a in avail_nodes}

        for tp in target_parents:
            target_nodes = search.findall(root, lambda node: (node.depth == node_depth) & (node.parent == tp))
            total_size = 0

            for tn in target_nodes:
                total_size += tn.size

            tp.size = total_size

        node_depth -= 1

    all_dir = search.findall_by_attr(root, name='type',value='dir')

    grand_total = 0
    for ad in all_dir:
        if ad.size <= 100000:
            grand_total += ad.size

    return grand_total


INPUT_S = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
EXPECTED = 95437


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

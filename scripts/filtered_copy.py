#!/usr/bin/env python3

import argparse
import shutil
from collections import defaultdict
from pathlib import Path


def operation(
    *,
    path_in: Path,
    path_out: Path,
    path_ex: Path,
) -> None:
    parent2name = defaultdict(set)
    with path_ex.open() as inf:
        for line in inf:
            items = line[:-1].split("\t")
            assert len(items) == 2
            parent2name[items[0]].add(items[1])

    for p in path_in.glob("*/*.png"):
        parent: str = p.parent.name
        name: str = p.name

        if name in parent2name.get(parent, {}):
            continue

        if parent == "zundamon_sd":
            parent = "zundamon"

        op = path_out.joinpath(parent)
        op.mkdir(parents=True, exist_ok=True)
        shutil.copy(p, op)


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--input", "-i", type=Path, required=True)
    oparser.add_argument("--output", "-o", type=Path, required=True)
    oparser.add_argument("--exclude", "--ex", type=Path, required=True)

    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    operation(
        path_in=opts.input,
        path_out=opts.output,
        path_ex=opts.exclude,
    )


if __name__ == "__main__":
    main()

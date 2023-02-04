#!/usr/bin/env python3

import argparse
import json
from collections import defaultdict
from pathlib import Path


def operation(
    *,
    path_in: Path,
    path_out: Path,
) -> None:
    fname2items = {}

    for item in path_in.iterdir():
        if not item.name.endswith(".txt"):
            continue
        with item.open() as inf:
            keywords = inf.read().strip().split(", ")
            fname2items[item.stem] = keywords

    with path_out.open("w") as outf:
        outf.write(
            json.dumps(
                fname2items,
                indent=4,
                sort_keys=True,
                ensure_ascii=False,
            )
        )
        outf.write("\n")


def count(
    *,
    path_in: Path,
    path_ref: Path,
    path_out: Path,
):
    path_out.mkdir(exist_ok=True, parents=True)
    with path_in.open() as rf:
        fname2items = json.load(rf)

    for target in path_ref.iterdir():
        if not target.is_dir():
            pass
        tag2count = defaultdict(int)
        for f in target.iterdir():
            items = fname2items[f.stem]
            for item in items:
                tag2count[item] += 1

        with path_out.joinpath(f"{target.name}.tsv").open("w") as outf:
            for k, v in sorted(tag2count.items(), key=lambda x: (-x[1], x[0])):
                outf.write(f"{k}\t{v}\n")


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--input", "-i", type=Path, default="/dev/stdin", required=False)
    oparser.add_argument("--output", "-o", type=Path, default="/dev/stdout", required=False)
    oparser.add_argument("--ref", type=Path)
    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    if opts.ref:
        count(
            path_in=opts.input,
            path_ref=opts.ref,
            path_out=opts.output,
        )
    else:
        operation(
            path_in=opts.input,
            path_out=opts.output,
        )


if __name__ == "__main__":
    main()

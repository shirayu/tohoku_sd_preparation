#!/usr/bin/env python3

import argparse
import random
import shutil
from pathlib import Path


def name2prompt(name: str) -> str:
    items = name.split("_")
    prompt = ["1girl"]

    t: str = items[0]
    prompt.append(t)

    if "fairy" in items:
        prompt[-1] += "_fairy"
    if "sd" in items:
        prompt[-1] += "_sd"

    if "oc" in items:
        prompt.append(f"{t}_oc")

    return ", ".join(prompt)


def operation(
    *,
    path_in: Path,
    path_out: Path,
    num_min: int,
    num_max: int,
    seed: int,
    num_repeat: int,
) -> None:
    assert num_min < num_max
    assert path_in.is_dir()
    random.seed(seed)

    for path_target_dir in path_in.iterdir():
        files = [fp for fp in path_target_dir.iterdir()]
        if len(files) < num_min:
            continue

        out_dir_name: str = f"{num_repeat}_" + name2prompt(path_target_dir.name)
        out_dir: Path = path_out.joinpath(out_dir_name)
        out_dir.mkdir(exist_ok=True, parents=True)

        target_files = random.sample(files, k=min(len(files), num_max))

        for tgt in target_files:
            print(f"{tgt} -> {out_dir}")
            shutil.copy(tgt, out_dir)


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--input", "-i", type=Path, required=True)
    oparser.add_argument("--output", "-o", type=Path, required=True)
    oparser.add_argument("--min", type=int, default=4)
    oparser.add_argument("--max", type=int, default=16)
    oparser.add_argument("--seed", type=int, default=42)
    oparser.add_argument("--repeat", type=int, default=1)
    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    operation(
        path_in=opts.input,
        path_out=opts.output,
        num_min=opts.min,
        num_max=opts.max,
        seed=opts.seed,
        num_repeat=opts.repeat,
    )


if __name__ == "__main__":
    main()

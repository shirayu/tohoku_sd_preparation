#!/usr/bin/env python3

import argparse
import shutil
from pathlib import Path
from typing import Optional

name2newname = {
    "melon": "hokamel",
    "zunko_oc": "zuoc",
    "kiritan_oc": "kioc",
    "itako_oc": "itoc",
}


def name2prompt(
    *,
    name: str,
    nosd: bool,
) -> Optional[str]:
    items = name.split("_")

    prompt: str = name2newname.get(items[0], items[0])

    if "fairy" in items:
        assert prompt == "zundamon"
        prompt = "zfr"
    if "sd" in items:
        prompt += "_sd"
        if nosd:
            return

    if "oc" in items:
        c: str = prompt.split("_")[0]
        assert c in {"zunko", "kiritan", "itako"}
        prompt = name2newname[f"{c}_oc"]


    return prompt


def operation(
    *,
    path_in: Path,
    path_out: Path,
    num_min: int,
    num: int,
    seed: int,
    num_repeat: int,
    nosd: bool,
    nodup: bool,
) -> None:
    assert num_min < num
    assert path_in.is_dir()

    for path_target_dir in path_in.iterdir():
        files = [fp for fp in path_target_dir.iterdir()]
        if len(files) < num_min:
            continue

        p = name2prompt(
            name=path_target_dir.name,
            nosd=nosd,
        )
        if p is None:
            continue
        out_dir_name: str = f"{num_repeat}_{p}"
        out_dir: Path = path_out.joinpath(out_dir_name)
        out_dir.mkdir(exist_ok=True, parents=True)

        done_count: int = 0
        while done_count < num:
            for tgt in files:
                to = out_dir.joinpath(f"{done_count:04}.png")
                print(f"{tgt} -> {to}")
                shutil.copy(tgt, to)
                done_count += 1
                if done_count >= num:
                    break
            if nodup:
                break


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--input", "-i", type=Path, required=True)
    oparser.add_argument("--output", "-o", type=Path, required=True)
    oparser.add_argument("--min", type=int, default=4)
    oparser.add_argument("--num", type=int, default=28)
    oparser.add_argument("--seed", type=int, default=42)
    oparser.add_argument("--repeat", type=int, default=1)
    oparser.add_argument("--nosd", action="store_true")
    oparser.add_argument("--nodup", action="store_true")
    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    operation(
        path_in=opts.input,
        path_out=opts.output,
        num_min=opts.min,
        num=opts.num,
        seed=opts.seed,
        num_repeat=opts.repeat,
        nosd=opts.nosd,
        nodup=opts.nodup,
    )


if __name__ == "__main__":
    main()

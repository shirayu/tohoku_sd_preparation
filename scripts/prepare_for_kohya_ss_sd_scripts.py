#!/usr/bin/env python3

import argparse
import json
import shutil
from pathlib import Path
from typing import List, Optional, Set

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
    seed: int,
    num_repeat: int,
    nosd: bool,
    nodup: bool,
    tag: Path,
    tag_target: Path,
) -> None:
    assert path_in.is_dir()

    with tag.open() as inf:
        name2tags = json.load(inf)

    with tag_target.open() as inf:
        chara2target_tags = json.load(inf)

    for path_target_dir in path_in.iterdir():
        files = [fp for fp in path_target_dir.iterdir()]

        chara = name2prompt(
            name=path_target_dir.name,
            nosd=nosd,
        )
        if chara is None or chara not in chara2target_tags:
            print(f"{chara}: SKIP!!")
            continue

        out_dir_name: str = f"{num_repeat}_{chara}"
        out_dir: Path = path_out.joinpath(chara, out_dir_name)
        out_dir.mkdir(exist_ok=True, parents=True)

        target_tags: Set[str] = set(chara2target_tags[chara])

        print(f"{chara}: {len(files)}")
        for tgt in files:
            tags: List[str] = name2tags[tgt.stem]
            tags = list(filter(lambda v: v not in target_tags, tags))
            tags.insert(0, chara)
            to_caption = out_dir.joinpath(f"{tgt.stem}.txt")
            with to_caption.open("w") as of:
                of.write(", ".join(tags))
                of.write("\n")

            to = out_dir.joinpath(f"{tgt.name}")
            shutil.copy(tgt, to)


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--input", "-i", type=Path, required=True)
    oparser.add_argument("--output", "-o", type=Path, required=True)
    oparser.add_argument("--tag", type=Path, required=True)
    oparser.add_argument("--tag-target", type=Path, required=True)
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
        seed=opts.seed,
        num_repeat=opts.repeat,
        nosd=opts.nosd,
        nodup=opts.nodup,
        tag=opts.tag,
        tag_target=opts.tag_target,
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
from pathlib import Path
from typing import Optional


def operation(
    *,
    path_in: Path,
    path_out: Path,
    path_model: Path,
    path_reg: Optional[Path],
    path_script_dir: Path,
    lr: str = "1e-4",
    unet_lr: str = "1e-4",
    text_encoder_lr: str = "1e-4",
    epoch: int = 10,
    dim: int = 64,
    resolution: str = "512,704",
    bs: int = 1,
) -> None:
    assert path_in.exists()
    assert path_script_dir.exists()
    assert path_script_dir.exists()
    path_out.mkdir(exist_ok=True, parents=True)

    for pathdir in path_in.iterdir():
        if not pathdir.is_dir():
            continue
        chara: str = pathdir.name
        path_out_chara = path_out.joinpath(chara)

        fullpath_model: str = str(path_model.absolute())
        fullpath_log: str = str(path_out_chara.joinpath("log").absolute())
        fullpath_train: str = str(pathdir.absolute())
        opt_fullpath_reg: str = ""
        if path_reg is not None:
            x = [z for z in path_reg.glob("*/*")]
            assert len(x) > 0, f"No files in {path_reg}"
            opt_fullpath_reg = f"--reg_data_dir={path_reg.absolute()}"

        CONTENT: str = f"""cd {path_script_dir.absolute()}

poetry run \\
    accelerate launch \\
    --num_processes 1 \\
    --num_machines 1 \\
    --mixed_precision "fp16" \\
    --dynamo_backend "no" \\
    train_network.py \\
    --pretrained_model_name_or_path={fullpath_model} \\
    --logging_dir={fullpath_log} \\
    --train_data_dir={fullpath_train} \\
    --output_dir={path_out_chara.absolute()} \\
    --prior_loss_weight=1.0 \\
    --train_batch_size={bs} \\
    --lr_warmup_steps=0 \\
    --lr_scheduler='constant' \\
    --learning_rate={lr} \\
    --unet_lr={unet_lr} \\
    --text_encoder_lr={text_encoder_lr} \\
    --max_train_epochs={epoch} \\
    --use_8bit_adam \\
    --xformers \\
    --mixed_precision=fp16 \\
    --save_every_n_epochs=1 \\
    --clip_skip=2 \\
    --seed=42 \\
    --network_dim={dim} \\
    --network_module=networks.lora \\
    --save_model_as=safetensors \\
    --save_precision="fp16" \\
    --resolution="{resolution}" \\
    --min_bucket_reso 256 \\
    --max_bucket_reso 1024 \\
    {opt_fullpath_reg} \\
    --enable_bucket \\
    --shuffle_caption \\
    --caption_extension=".txt" \\
    --keep_tokens 1 \\
    --max_data_loader_n_workers=4 \\
    --persistent_data_loader_workers
    """

        path_out_chara.mkdir(exist_ok=True, parents=True)
        with path_out_chara.joinpath(f"{pathdir.name}_train.sh").open("w") as outf:
            outf.write(CONTENT)


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--input", "-i", type=Path, required=True)
    oparser.add_argument("--output", "-o", type=Path, required=True)
    oparser.add_argument("--model", type=Path, required=True)
    oparser.add_argument("--reg", type=Path, required=True)
    oparser.add_argument("--script-dir", "-C", type=Path, required=True)

    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    operation(
        path_in=opts.input,
        path_out=opts.output,
        path_model=opts.model,
        path_reg=opts.reg,
        path_script_dir=opts.script_dir,
    )


if __name__ == "__main__":
    main()

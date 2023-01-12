
# tohoku_sd_preparation

## Setup images

```bash
# Install ImageMagick
sudo apt-get -y install imagemagic

# Edit the setting of ImageMagick
sudo vi /etc/ImageMagick-6/policy.xml 
## Before:
##   <policy domain="resource" name="memory" value="256MiB"/>
## After:
##   <policy domain="resource" name="memory" value="2560MiB"/>

# setup
poetry install

# Download images
poetry run python scripts/download.py -i ./url_list -o ./data/img_original 

# Remove alphas, margins and shrink images
find data/img_original -type f | xargs -t -P 4 -I {} bash ./scripts/convert_image_0.sh {} data/img_converted

# Check files in "img_converted" with your eyes

# Resize to 512x704
find data/img_converted -type f | xargs -t -P 4 -I {} bash ./scripts/convert_image_1.sh {} data/img_train_512x704 512x704
```

### Prefix

- ``_oc``: Official costume
- ``_sd``: SD character

## Preparation

```bash
python ./scripts/prepare_for_kohya_ss_sd_scripts.py -i ./data/img_train_512x704 -o ./data/dreambooth/img_train --nosd --repeat 3 --num 28
mkdir -p ./data/dreambooth/img_reg
```

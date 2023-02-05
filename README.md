
# tohoku_sd_preparation

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![CI](https://github.com/shirayu/tohoku_sd_preparation/actions/workflows/ci.yml/badge.svg)](https://github.com/shirayu/tohoku_sd_preparation/actions/workflows/ci.yml)
[![CodeQL](https://github.com/shirayu/tohoku_sd_preparation/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/shirayu/tohoku_sd_preparation/actions/workflows/codeql-analysis.yml)
[![Typos](https://github.com/shirayu/tohoku_sd_preparation/actions/workflows/typos.yml/badge.svg)](https://github.com/shirayu/tohoku_sd_preparation/actions/workflows/typos.yml)

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

# Filter out
python ./scripts/filtered_copy.py --ex ./target_list/exclude.tsv -i ./data/img_train_512x704 -o ./data/img_train_512x704_filtered

# Generate captions
python ./scripts/prepare_for_kohya_ss_sd_scripts.py -i ./data/img_train_512x704_filtered -o ./data/img_train_all --nosd --repeat 5 --tag ./data/tag/tag.json --tag-target ./data/tag/tag_target.json
```

### Prefix

- ``_oc``: Official costume
- ``_sd``: SD character

## Tags

```bash
mkdir -p data/tag
python ./scripts/tag2json.py -i /path/to/images -o ./data/tag/tag.json
python ./scripts/tag2json.py --ref ./data/img_train_512x704 -i ./data/tag/tag.json -o counted
```

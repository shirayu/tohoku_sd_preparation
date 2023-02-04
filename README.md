
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

## Tags

```bash
mkdir -p data/tag
python ./scripts/tag2json.py -i /path/to/images -o ./data/tag/tag.json
python ./scripts/tag2json.py --ref ./data/img_train_512x704 -i ./data/tag/tag.json -o counted
```

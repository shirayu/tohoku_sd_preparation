
# tohoku_sd_preparation

## Setup images

```bash
# setup
poetry install

# Download images
poetry run python scripts/download.py -i ./url_list -o ./data/img_original 

# Remove alphas, margins and shrink images
find data/img_original/ -type f | xargs -t  -P 2 -I {} bash ./scripts/convert_image_0.sh {} data/img_converted

# Check files in "img_converted" with  your eyes

# Resize to 512x512
mkdir train
find ./data/img_converted_selected/ -type f | grep '\.png$' | parallel -t convert -fuzz 5% -trim -resize 512x512 -gravity center -extent 512x512 {} train/{/.}.png
```

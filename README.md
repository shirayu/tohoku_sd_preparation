
# tohoku_sd_preparation


## 画像データの準備

1. ``https://zunko.jp/con_illust.html``から画像データを取得する
    - URLは``url_list``
2. アルファチャンネルを削除・余白削除・画像サイズ縮小

    ```bash
    find data/img_original/ -type f | xargs -t  -P 2 -I {} bash ./scripts/convert_image_0.sh {} img_converted
    ```

3. ``img_converted``の画像に問題がないことを目視で確認する
4. 512x512にトリミングする

    ```bash
    mkdir train
    find ./data/img_converted_selected/ -type f | grep '\.png$' | parallel -t convert -fuzz 5% -trim -resize 512x512 -gravity center -extent 512x512 {} train/{/.}.png
    ```

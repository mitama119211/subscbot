# subscbot

Youtubeチャンネル登録者数を取得しツイートする。

## 更新履歴

- ver 1.0
初版作成
- ver 2.0
大幅に変更。tweet_subscribersのデフォルトを画像ツイートに。

## 動作環境

- Python 3.6+

## 事前に必要なもの

- Twitter Developerアカウント
  - Access token
  - Access token secret
- Youtube Data APIのAPIキー

## セットアップ

1. 仮想環境作成

    ```bash
    $ cd env

    # venv実行
    $ make

    ```

2. chinfo.csvの作成

    チャンネルID、ユーザ名、ディレクトリ名の情報を含むcsvファイルを作成。
    - chid: youtubeチャンネル固有のID。チャンネルトップのURLの`channel/`以下の部分。
    - name: ハッシュタグで用いる名前。
    - dirname: ログ出力先の名前。twitter IDなどを参考に。

    例：

    ```csv
    chid,name,dirname
    UCLhUvJ_wO9hOvv_yYENu4fQ,電脳少女シロ,SIROyoutuber
    UCz6Gi81kE6p5cdW1rT0ixqw,もこ田めめめ,mokomeme_ch
    ```

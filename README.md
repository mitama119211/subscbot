# subscbot

Youtubeチャンネル登録者数を取得しツイートする．

## 更新履歴

- ver 1.0
初版作成
- ver 2.0
大幅に変更．tweet_subscribersのデフォルトを画像ツイートに．
- ver 2.1
一部の仕様を変更．ドキュメントなどを追記．
- ver 2.2
API keyなどの設定をyamlフォーマットのファイルで管理するように変更．

## 動作環境

- Python 3.6+

## 事前に必要なもの

- Twitter Developerアカウントとそのアプリ
  - API key
  - API key secret
- Youtube Data API v3のAPIキー

## セットアップ

1. 仮想環境作成

    ```bash
    $ cd env

    # venv実行
    $ make

    ```

2. chinfo.csv作成

    チャンネルID，ユーザ名，ディレクトリ名の情報を含むcsvファイルを作成．
    - chid: youtubeチャンネル固有のID．チャンネルトップのURLの`channel/`以下の部分．
    - name: ハッシュタグで用いる名前．
    - dirname: ログ出力先の名前．twitter IDなどを参考に．

    例：

    ```csv
    chid,name,dirname
    UCLhUvJ_wO9hOvv_yYENu4fQ,電脳少女シロ,SIROyoutuber
    UCz6Gi81kE6p5cdW1rT0ixqw,もこ田めめめ,mokomeme_ch
    ```

3. API_KEY，API_KEY_SECRET，DEVELOPER_KEYを設定

    `conf/config.yaml`の`API_KEY=""`，`API_KEY_SECRET=""`にTwitter Developerアカウントで作成したアプリのAPI key，API key secretをそれぞれ記述．
    また，`DEVELOPER_KEY=""`にYoutube Data API v3のAPIキーを記述．

4. authenticate.shを実行し，ACCESS_TOKEN，ACCESS_TOKEN_SECRETを取得
  
5. ACCESS_TOKEN，ACCESS_TOKEN_SECRETを設定
    `conf/config.yaml`の`ACCESS_TOKEN=""`，`ACCESS_TOKEN_SECRET=""`に取得した値をそれぞれ記述．

## Reference

- [API reference index — Twitter Developers](https://developer.twitter.com/en/docs/api-reference-index)
- [Twitter REST APIの使い方](https://syncer.jp/Web/API/Twitter/REST_API/)

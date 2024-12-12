# picol-flask

docker compose を用いて起動してください

```bash
# flaskサーバーをビルド
docker compose build

# コンテナを起動
docker compose up -d
```

サーバーは gunicorn を用いて起動されます

注：requirements.txt を変更した場合は、再ビルドをする必要があります

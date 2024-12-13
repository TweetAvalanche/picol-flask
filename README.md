# picol-flask

docker compose を用いて起動してください

```bash
docker compose up -d --build
```

サーバーは gunicorn を用いて起動されます

注：requirements.txt を変更した場合は、再ビルドをする必要があります

ビルドに失敗するようになった場合は、以下を実行してキャッシュを削除してみてください

```bash
docker builder prune
```

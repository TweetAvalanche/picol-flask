# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係をコピーしてインストール
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー
COPY app/ .

# ポートを公開
EXPOSE 5000

# アプリケーションを実行
CMD ["python", "app.py"]

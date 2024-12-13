# ベースイメージ
FROM python:3.9-slim

# 必要なライブラリをインストール
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0

# 作業ディレクトリを指定
WORKDIR /app

# ローカルファイルをイメージへコピー
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5012

CMD ["gunicorn", "-b", "0.0.0.0:5012", "server:app"]

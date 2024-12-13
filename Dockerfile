# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリを指定
WORKDIR /app

# OpenCVのインストール
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxrender1 libxext6 && \
    rm -rf /var/lib/apt/lists/*

# ローカルファイルをイメージへコピー
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5012

CMD ["gunicorn", "-b", "0.0.0.0:5012", "server:app"]

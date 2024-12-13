# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリを指定
WORKDIR /app

# 必要なシステムライブラリをインストール
RUN apt-get update && apt-get install -y libgl1 && apt-get clean

# ローカルファイルをイメージへコピー
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5012

CMD ["gunicorn", "-b", "0.0.0.0:5012", "server:app"]

# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリを指定
WORKDIR /app

# ローカルファイルをイメージへコピー
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "run.py"]

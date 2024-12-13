# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリを指定
WORKDIR /app

# OpenCVのインストール
FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

RUN apt-get -y update && \
    apt-get install -y build-essential g++-8 libopenblas-dev \
            libgtk2.0-dev pkg-config python-dev python-numpy \
            libgl1-mesa-dev
RUN curl -kL https://bootstrap.pypa.io/get-pip.py | python3

# ローカルファイルをイメージへコピー
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5012

CMD ["gunicorn", "-b", "0.0.0.0:5012", "server:app"]

#!/bin/bash

# IMAGE名を指定
TARGET_IMAGE="picol-flask-flask"

# docker ps で指定されたIMAGE名のコンテナIDを取得
CONTAINER_ID=$(docker ps --filter "ancestor=$TARGET_IMAGE" --format "{{.ID}}")

# コンテナが見つからない場合の処理
if [ -z "$CONTAINER_ID" ]; then
    echo "No running container found for image: $TARGET_IMAGE"
    exit 1
fi

# コンテナログを表示
echo "Logs for container ID: $CONTAINER_ID"
docker logs "$CONTAINER_ID"

import requests
import os
import json

# テスト用のエンドポイントURL
url = "http://127.0.0.1:5000/image/analyze"

# 送信する画像ファイル
dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"
file_path = "funfes2024-1.png"

with open(dir_path + file_path, 'rb') as f:
    files = {'image': f}
    response = requests.post(url, files=files)

print("--------------------------------")
print("ファイル名:", file_path)
print("リクエスト:", "POST", url)
# 結果を表示
print("ステータスコード:", response.status_code)
print("レスポンス:", json.dumps(response.json(), indent=4, ensure_ascii=False))

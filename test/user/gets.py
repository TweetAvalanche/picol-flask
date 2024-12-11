import requests
import json

# テスト用のエンドポイントURL
url = "http://127.0.0.1:5000/user"

response = requests.get(url)

print("--------------------------------")
print("リクエスト:", "GET", url)
# 結果を表示
print("ステータスコード:", response.status_code)
print("レスポンス:", response._content.decode('utf-8'))

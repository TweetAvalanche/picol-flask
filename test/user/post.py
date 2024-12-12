import requests

# テスト用のエンドポイントURL
url = 'http://localhost:5000/user'

# POSTリクエストを送信
response = requests.post(url)

# レスポンスの内容を表示
print(f"Status Code: {response.status_code}")
print(f"Response JSON: {response.json()}")

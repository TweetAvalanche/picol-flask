import requests
import random
import string

url = 'http://localhost:5000/user'  # FlaskアプリのURL

# テストデータ
data = {
    'level': 1
}

# POSTリクエストを送信
response = requests.post(url, json=data)

# レスポンスの内容を表示
print(f"Status Code: {response.status_code}")
print(f"Response JSON: {response.json()}")

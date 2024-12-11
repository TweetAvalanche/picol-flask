import requests
import random
import string

url = 'http://localhost:5000/user'  # FlaskアプリのURL

# ランダムな12文字のユーザー名を生成
user_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))

# テストデータ
data = {
    'user_id': user_id,
    'level': 1
}

# POSTリクエストを送信
response = requests.post(url, json=data)

# レスポンスの内容を表示
print(f"Status Code: {response.status_code}")
print(f"Response JSON: {response.json()}")

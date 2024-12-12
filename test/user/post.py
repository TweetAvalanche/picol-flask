import requests

# テスト用のエンドポイントURL
url = 'http://localhost:5012/user'

# POSTリクエストを送信
response = requests.post(url)

# 結果を表示
print("--------------------------------")
print("リクエスト:", "POST", url)
print("ステータスコード:", response.status_code)
print("レスポンス:", response._content.decode('unicode-escape'))

import requests

uid = input("ユーザーIDを入力してください: ")

# テスト用のエンドポイントURL
url = f"http://127.0.0.1:5012/token?uid={uid}"

# POSTリクエストを送信
response = requests.post(url)

# 結果を表示
print("--------------------------------")
print("リクエスト:", "POST", url)
print("ステータスコード:", response.status_code)
print("レスポンス:", response._content.decode('unicode-escape'))

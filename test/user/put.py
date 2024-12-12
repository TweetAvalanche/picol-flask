import requests

uid = input("ユーザーIDを入力してください: ")
message = input("メッセージを入力してください: ")

# テスト用のエンドポイントURL
url = f"http://127.0.0.1:5000/user?uid={uid}&message={message}"

response = requests.put(url)

# 結果を表示
print("--------------------------------")
print("リクエスト:", "PUT", url)
print("ステータスコード:", response.status_code)
print("レスポンス:", response._content.decode('unicode-escape'))

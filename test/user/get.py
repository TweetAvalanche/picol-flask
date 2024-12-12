import requests

uid = input("ユーザーIDを入力してください: ")

# テスト用のエンドポイントURL
url = f"http://127.0.0.1:5000/user/{uid}"

response = requests.get(url)

print("--------------------------------")
print("リクエスト:", "GET", url)
# 結果を表示
print("ステータスコード:", response.status_code)
print("レスポンス:", response._content.decode('unicode-escape'))

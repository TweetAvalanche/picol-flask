import requests

uid = input("ユーザーIDを入力してください: ")
cid = input("CIDを入力してください: ")

# テスト用のエンドポイントURL
url = f"http://127.0.0.1:5012/character/default?uid={uid}&cid={cid}"

response = requests.put(url)

# 結果を表示
print("--------------------------------")
print("リクエスト:", "PUT", url)
print("ステータスコード:", response.status_code)
print("レスポンス:", response._content.decode('unicode-escape'))

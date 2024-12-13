import requests

cid = input("CIDを入力してください: ")

# テスト用のエンドポイントURL
url = f"http://127.0.0.1:5012/character/all?cid={cid}"

response = requests.get(url)

# 結果を表示
print("--------------------------------")
print("リクエスト:", "GET", url)
print("ステータスコード:", response.status_code)
print("レスポンス:", response._content.decode('unicode-escape'))

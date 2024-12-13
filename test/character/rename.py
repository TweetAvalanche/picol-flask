import requests

cid = input("CIDを入力してください: ")
character_name = input("名前を入力してください: ")

# テスト用のエンドポイントURL
url = f"http://127.0.0.1:5012/character/rename?cid={cid}&character_name={character_name}"

response = requests.put(url)

# 結果を表示
print("--------------------------------")
print("リクエスト:", "PUT", url)
print("ステータスコード:", response.status_code)
print("レスポンス:", response._content.decode('unicode-escape'))

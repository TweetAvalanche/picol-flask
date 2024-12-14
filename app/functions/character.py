from mysql.connector import Error
from .character_defs import generate_character
from ..mysql import get_db_connection
import base64

def get_character_2(cid):

    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn # エラーメッセージを返す
    
    try:
        cursor = conn.cursor(dictionary=True)
        # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
        cursor.execute("SELECT * FROM characters WHERE cid = %s", (cid,))
        character = cursor.fetchone()
        cursor.close()
        conn.close()
        if character:
            response = {
                "character_param": character["character_param"],
                "character_name": character["character_name"],
            }
            print(response)
            return response
        else:
            error_response = {"error": "character not found", "status": 404}
            print(error_response)
            return error_response
    except Error as err:
        error_response = {"error": str(err), "status": 500}
        print(error_response)
        return error_response

def get_user_function(uid):

    # 値なしエラー
    if not uid:
        error_response = {"error": "Missing uid", "status": 400}
        print(error_response)
        return error_response
    
    # 型検証
    if not isinstance(uid, int):
        error_response = {"error": "uid must be an integer", "status": 400}
        print(error_response)
        return error_response

    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す

    try:
        cursor = conn.cursor(dictionary=True)
        # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
        cursor.execute("SELECT * FROM users WHERE uid = %s", (uid,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            cid = user['cid']
            if cid == 0:
                response = {
                    "uid": uid,
                    "user_message": user['message'],
                    "cid": 0,
                    "character_name": "",
                    "character_param": "",
                    "character_aura_image": "",
                    "status": 200
                }
                print(response)
                return response
            else:
                character = get_character_2(cid)
                response = {
                    "uid": uid,
                    "user_message": user['message'],
                    "cid": cid,
                    "character_name": character['character_name'],
                    "character_param": character['character_param'],
                    "character_aura_image": "",
                    "status": 200
                }
                print(response)
                return response
        else:
            error_response = {"error": "user not found", "status": 404}
            print(error_response)
            return error_response
    except Error as err:
        error_response = {"error": str(err), "status": 500}
        print(error_response)
        return error_response

# !キャラクターの追加
def add_character_function(file, uid):

    raw_image = base64.b64encode(file.read()).decode('utf-8')
    
    # ファイルポインタを先頭にリセット
    file.seek(0)
    
    # デバッグ用のログ出力を追加
    print(f"raw_image: {raw_image[:100]}...")  # 画像データの最初の100文字を表示

    character = generate_character(file)

    # パラメータの取得
    character_param = character["character_param"]
    character_name = "ぴこるー"
    character_aura_image = character["character_aura_image"]

    # 値なしエラー
    if not uid:
        error_response = {"error": "Missing uid", "status": 400}
        print(error_response)
        return error_response
    if not character_param:
        error_response = {"error": "Missing character_param", "status": 400}
        print(error_response)
        return error_response
    if not character_name:
        error_response = {"error": "Missing character_name", "status": 400}
        print(error_response)
        return error_response
    if not character_aura_image:
        error_response = {"error": "Missing character_aura_image", "status": 400}
        print(error_response)
        return error_response
    if not raw_image:
        error_response = {"error": "Missing raw_image", "status": 400}
        print(error_response)
        return error_response
    
    # 型検証
    if not isinstance(uid, int):
        error_response = {"error": "uid must be an integer", "status": 400}
        print(error_response)
        return error_response

    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO characters (uid, character_param, character_name, raw_image)
            VALUES (%s, %s, %s, %s)
        """, (uid, character_param, character_name, raw_image))
        conn.commit()
        cid = cursor.lastrowid
        cursor.close()
        conn.close()
        set_default_character_function(cid)
        user = get_user_function(uid)
        response = {
            "uid": uid,
            "user_message": user["user_message"],
            "cid": cid,
            "character_name": character_name,
            "character_param": character_param,
            "character_aura_image": "",
            "status": 200
        }
        print(response)
        return response
    except Error as err:
        error_response = {"error": str(err), "status": 500}
        print(error_response)
        return error_response

# !キャラクターの取得
def get_character_function(cid):
    
    # 値なしエラー
    if not cid:
        response = {
            "uid": 1,
            "user_message": "キャラクターが作成されていないためユーザーを検索できません",
            "cid": 0,
            "character_param": "1ff2222",
            "character_name": "デフォルトキャラクター・ゼロ",
            "character_aura_image": "",
            "status": 200
        }
        print(response)
        return response
    
    # 型検証
    if not isinstance(cid, int):
        error_response = {"error": "cid must be an integer", "status": 400}
        print(error_response)
        return error_response
    
    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn # エラーメッセージを返す
    
    try:
        cursor = conn.cursor(dictionary=True)
        # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
        cursor.execute("SELECT * FROM characters WHERE cid = %s", (cid,))
        character = cursor.fetchone()
        cursor.close()
        conn.close()
        if character:
            uid = character["uid"]
            user = get_user_function(uid)
            character_aura_image = character["character_aura_image"] if "character_aura_image" in character else ""
            response = {
                "uid": uid,
                "user_message": user["user_message"],
                "cid": cid,
                "character_param": character["character_param"],
                "character_name": character["character_name"],
                "character_aura_image": "",
                "status": 200
            }
            print(response)
            return response
        else:
            error_response = {"error": "character not found", "status": 404}
            print(error_response)
            return error_response
    except Error as err:
        error_response = {"error": str(err), "status": 500}
        print(error_response)
        return error_response
    
# !全キャラクターの取得
def get_all_characters_function(uid):
    
    # 値なしエラー
    if not uid:
        error_response = {"error": "Missing uid", "status": 400}
        print(error_response)
        return error_response
    
    # 型検証
    if not isinstance(uid, int):
        error_response = {"error": "uid must be an integer", "status": 400}
        print(error_response)
        return error_response
    
    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn
    
    try:
        cursor = conn.cursor(dictionary=True)
        # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
        cursor.execute("SELECT * FROM characters WHERE uid = %s", (uid,))
        characters = cursor.fetchall()
        cursor.close()
        conn.close()
        response = []
        for character in characters:
            uid = character["uid"]
            user = get_user_function(uid)
            response.append({
                "uid": uid,
                "user_message": user["user_message"],
                "cid": character["cid"],
                "character_param": character["character_param"],
                "character_name": character["character_name"],
                "character_aura_image": "",
            })
        response["status"] = 200
        print(response)
        return response
    except Error as err:
        error_response = {"error": str(err), "status": 500}
        print(error_response)
        return error_response

# !キャラクターのリネーム
def rename_character_function(cid, character_name, make_default):
    # 値なしエラー
    if not cid:
        error_response = {"error": "Missing cid", "status": 400}
        print(error_response)
        return error_response
    if not character_name:
        error_response = {"error": "Missing character_name", "status": 400}
        print(error_response)
        return error_response

    # 型検証
    if not isinstance(cid, int):
        error_response = {"error": "cid must be an integer", "status": 400}
        print(error_response)
        return error_response

    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す

    try:
        cursor = conn.cursor()
        # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
        cursor.execute("""
            UPDATE characters
            SET character_name = %s
            WHERE cid = %s
        """, (character_name, cid))
        conn.commit()
        cursor.close()
        conn.close()
        if make_default:
            return set_default_character_function(cid)
        else:
            response = get_character_function(cid)
            response["status"] = 200
            print(response)
            return response
    except Error as err:
        error_response = {"error": str(err), "status": 500}
        print(error_response)
        return error_response

def set_default_character_function(cid):
    
    # 値なしエラー
    if not cid:
        error_response = {"error": "Missing cid", "status": 400}
        print(error_response)
        return error_response

    # 型検証
    if not isinstance(cid, int):
        error_response = {"error": "cid must be an integer", "status": 400}
        print(error_response)
        return error_response
    
    character = get_character_function(cid)
    uid = character["uid"]

    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す

    try:
        cursor = conn.cursor(dictionary=True)
        # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
        cursor.execute("""
            UPDATE users
            SET cid = %s
            WHERE uid = %s
        """, (cid, uid))
        conn.commit()
        cursor.close()
        conn.close()
        response = get_character_function(cid)
        response["status"] = 200
        print(response)
        return response
    except Error as err:
        error_response = {"error": str(err), "status": 500}
        print(error_response)
        return error_response

def get_character_raw_function(cid):
    
    # 値なしエラー
    if not cid:
        response = {
            "uid": 1,
            "user_message": "キャラクターが作成されていないためユーザーを検索できません",
            "cid": 0,
            "character_param": "1ff2222",
            "character_name": "デフォルトキャラクター・ゼロ",
            "character_aura_image": "",
            "status": 200
        }
        print(response)
        return response
    
    # 型検証
    if not isinstance(cid, int):
        error_response = {"error": "cid must be an integer", "status": 400}
        print(error_response)
        return error_response
    
    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn # エラーメッセージを返す
    
    try:
        cursor = conn.cursor(dictionary=True)
        # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
        cursor.execute("SELECT * FROM characters WHERE cid = %s", (cid,))
        character = cursor.fetchone()
        cursor.close()
        conn.close()
        if character:
            uid = character["uid"]
            response = {
                "raw_image": character["raw_image"],
                "status": 200
            }
            print(response)
            return response
        else:
            error_response = {"error": "character not found", "status": 404}
            print(error_response)
            return error_response
    except Error as err:
        error_response = {"error": str(err), "status": 500}
        print(error_response)
        return error_response

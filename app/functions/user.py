from mysql.connector import Error
from ..mysql import get_db_connection
from .character import get_character_function

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
            cid = user['default_cid']
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
                character = get_character_function(cid)
                response = {
                    "uid": uid,
                    "user_message": user['message'],
                    "cid": cid,
                    "character_name": character['character_name'],
                    "character_param": character['character_param'],
                    "character_aura_image": character['character_aura_image'],
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

def update_user_function(uid, message):
    
    # 値なしエラー
    if not uid:
        error_response = {"error": "Missing uid", "status": 400}
        print(error_response)
        return error_response
    if not message:
        error_response = {"error": "Missing message", "status": 400}
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
        # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
        cursor.execute("UPDATE users SET message = %s WHERE uid = %s", (message, uid))
        conn.commit()
        cursor.close()
        conn.close()
        user = get_user_function(uid)
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
            character = get_character_function(cid)
            response = {
                "uid": uid,
                "user_message": user['message'],
                "cid": cid,
                "character_name": character['character_name'],
                "character_param": character['character_param'],
                "character_aura_image": character['character_aura_image'],
                "status": 200
            }
            print(response)
            return response
    except Error as err:
        error_response = {"error": str(err), "status": 500}
        print(error_response)
        return error_response

    
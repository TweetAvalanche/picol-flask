from mysql.connector import Error
import random
import string
from datetime import datetime, timedelta
from ..mysql import get_db_connection
from .user import get_user_function
from .character import get_character_function


def create_token_function(uid):
    # 値なしエラー
    if not uid:
        error_response = {"error": "uid is required", "status": 400}
        print(error_response)
        return error_response

    # 型検証
    if not isinstance(uid, int):
        error_response = {"error": "uid must be an integer", "status": 400}
        print(error_response)
        return error_response

    # トークンの生成
    token = "".join(random.choices(string.hexdigits[:16], k=6))
    expire_at = datetime.now() + timedelta(hours=1)
    
    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す

    try:
        cursor = conn.cursor()
        # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
        cursor.execute(
            """
            INSERT INTO tokens (token, uid, expire_at, is_valid)
            VALUES (%s, %s, %s, TRUE)
        """,
            (token, uid, expire_at),
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Error as err:
        error_response = {"error": str(err), "status": 500}
        print(error_response)
        return error_response
    
    response = {"token": token, "status": 200}

    print(response)
    return response

def check_token_function(token):
    # 値なしエラー
    if not token:
        error_response = {"error": "token is required", "status": 400}
        print(error_response)
        return error_response

    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す
    
    try:
        cursor = conn.cursor(dictionary=True)
        # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
        cursor.execute("SELECT * FROM tokens WHERE token = %s", (token,))
        token_data = cursor.fetchone()
        
        if token_data and token_data["is_valid"]:
            # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
            cursor.execute("UPDATE tokens SET is_valid = FALSE WHERE token = %s", (token,))
            conn.commit()
        elif token_data and not token_data["is_valid"]:
            token_data = None
        
        cursor.close()
        conn.close()
    except Error as err:
        error_response = {"error": str(err), "status": 500}
        print(error_response)
        return err
    
    if token_data:
        uid = int(token_data["uid"])
        user = get_user_function(uid)
        character = get_character_function(user["cid"])
        response = {
            "uid": uid,
            "user_message": user["user_message"],
            "cid": character["cid"],
            "character_name": character["character_name"],
            "character_param": character["character_param"],
            "character_aura_image": character["character_aura_image"],
            "status": 200
        }
        print(response)
        return response
    else:
        error_response = {"error": "token not found or not valid", "status": 404}
        print(error_response)
        return error_response

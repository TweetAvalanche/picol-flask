from flask import Blueprint, request, jsonify
from mysql.connector import Error
import random
import string
from datetime import datetime, timedelta
from .mysql import get_db_connection
from .user import get_user
from .character import get_character
import json

token_bp = Blueprint('token', __name__)

# !トークンの生成
@token_bp.route("/", methods=["POST"])
def create_token():
    # パラメータの取得
    uid = int(request.args.get('uid'))

    # 値なしエラー
    if not uid:
        error_response = {"error": "uid is required"}
        print(error_response)
        return jsonify(error_response), 400
    
    # 型検証
    if not isinstance(uid, int):
        error_response = {"error": "uid must be an integer"}
        print(error_response)
        return jsonify(error_response), 400

    # トークンの生成
    token = ''.join(random.choices(string.hexdigits[:16], k=6))
    expire_at = datetime.now() + timedelta(hours=1)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
        cursor.execute("""
            INSERT INTO tokens (token, uid, expire_at, is_valid)
            VALUES (%s, %s, %s, TRUE)
        """, (token, uid, expire_at))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as err:
        error_response = {"error": str(err)}
        print(error_response)
        return jsonify(error_response), 500

    print({"token": token})
    return jsonify({"token": token})

# !トークンの検証
@token_bp.route("/", methods=["GET"])
def check_token():
    # パラメータの取得
    token = request.args.get('token')

    # 値なしエラー
    if not token:
        error_response = {"error": "token is required"}
        print(error_response)
        return jsonify(error_response), 400

    try:
        conn = get_db_connection()
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
        error_response = {"error": str(err)}
        print(error_response)
        return jsonify(error_response), 500
    if token_data:
        uid = int(token_data["uid"])
        user_json = get_user(uid)
        user = json.loads(user_json)
        character_json = get_character(user["default_cid"])
        character = json.loads(character_json)
        response = {
            "uid": uid,
            "user_message": user["user_message"],
            "cid": character["cid"],
            "character_name": character["character_name"],
            "character_param": character["character_param"],
            "character_aura_image": character["character_aura_image"]
        }
        print(response)
        return jsonify(response)
    else:
        error_response = {"error": "token not found or not valid"}
        print(error_response)
        return jsonify(error_response), 404

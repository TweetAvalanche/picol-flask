from flask import Blueprint, request, jsonify
from mysql.connector import Error
import random
import string
from datetime import datetime, timedelta
from .mysql import get_db_connection
from .user import get_user
from .character import get_character

token_bp = Blueprint('token', __name__)



@token_bp.route("/", methods=["POST"])
def create_token():
    # パラメータの取得
    uid = int(request.args.get('uid'))

    # 値なしエラー
    if not uid:
        return jsonify({"error": "uid is required"}), 400
    
    # 型検証
    if not isinstance(uid, int):
        return jsonify({"error": "uid must be an integer"}), 400
    

    # トークンの生成
    token = ''.join(random.choices(string.hexdigits[:16], k=6))
    expire_at = datetime.now() + timedelta(hours=1)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tokens (token, uid, expire_at, is_valid)
            VALUES (%s, %s, %s, TRUE)
        """, (token, uid, expire_at))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"token": token})

@token_bp.route("/", methods=["GET"])
def check_token():
    # パラメータの取得
    token = request.args.get('token')

    # 値なしエラー
    if not token:
        return jsonify({"error": "token is required"}), 400
    
    # SQLインジェクション対策
    if ";" in token or "--" in token or "'" in token or "\"" in token:
        return jsonify({"error": "Invalid characters in token"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tokens WHERE token = %s", (token,))
        token_data = cursor.fetchone()
        
        if token_data and token_data["is_valid"]:
            cursor.execute("UPDATE tokens SET is_valid = FALSE WHERE token = %s", (token,))
            conn.commit()
        elif token_data and not token_data["is_valid"]:
            token_data = None
        
        cursor.close()
        conn.close()
    except Error as e:
        return jsonify({"error": str(e)}), 500
    if token_data:
        uid = int(token_data["uid"])
        user = get_user(uid)
        character = get_character(user["default_cid"])
        response = {
            "uid": uid,
            "user_message": user["user_message"],
            "cid": character["cid"],
            "character_name": character["character_name"],
            "character_param": character["character_param"],
            "character_aura_image": character["character_aura_image"]
        }
        return jsonify(response)
    else:
        return jsonify({"error": "token not found or not valid"}), 404

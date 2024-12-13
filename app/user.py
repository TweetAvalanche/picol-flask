from flask import Blueprint, request, jsonify
from mysql.connector import Error
from .mysql import get_db_connection

user_bp = Blueprint('user', __name__)

# !ユーザー情報の追加
@user_bp.route('/', methods=['POST'])
def add_user():

    default_message = "こんにちは"

    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す

    try:
        cursor = conn.cursor()
        # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
        cursor.execute("INSERT INTO users (message) VALUES (%s)", (default_message,))
        conn.commit()
        uid = cursor.lastrowid
        cursor.close()
        conn.close()
        response = {
            "uid": uid,
            "user_message": default_message,
            "cid": 0,
            "character_name": "NOT_IMPLEMENTED",
            "character_param": "NOT_IMPLEMENTED"
        }
        return jsonify(response), 201
    except Error as err:
        return jsonify({"error": str(err)}), 500

# !ユーザー情報の取得
@user_bp.route('/', methods=['GET'])
def get_user(uid = None):
    
    # パラメータの取得
    if uid is None:
        uid = request.args.get('uid', type=int)

    # 値なしエラー
    if not uid:
        return jsonify({"error": "Missing uid"}), 400
    
    # 型検証
    if not isinstance(uid, int):
        return jsonify({"error": "uid must be an integer"}), 400

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
            response = {
                "uid": uid,
                "user_message": user["message"],
                "cid": 0,
                "character_name": "NOT_IMPLEMENTED",
                "character_param": "NOT_IMPLEMENTED"
            }
            return jsonify(response), 200
        else:
            return jsonify({"error": "user not found"}), 404
    except Error as err:
        return jsonify({"error": str(err)}), 500

# !ユーザー情報の更新
@user_bp.route('/', methods=['PUT'])
def update_user():
    # パラメータの取得
    uid = request.args.get('uid', type=int)
    message = request.args.get('message', type=str)

    # 値なしエラー
    if not uid:
        return jsonify({"error": "Missing uid"}), 400
    if not message:
        return jsonify({"error": "Missing message"}), 400
    
    # 型検証
    if not isinstance(uid, int):
        return jsonify({"error": "uid must be an integer"}), 400
    if not isinstance(message, str):
        return jsonify({"error": "message must be a string"}), 400
    
    # SQLインジェクション対策
    if ";" in message or "--" in message or "'" in message or "\"" in message:
        return jsonify({"error": "Invalid characters in message"}), 400

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
        response = {
            "uid": uid,
            "user_message": message,
            "cid": 0,
            "character_name": "NOT_IMPLEMENTED",
            "character_param": "NOT_IMPLEMENTED"
        }
        return jsonify(response), 200
    except Error as err:
        return jsonify({"error": str(err)}), 500

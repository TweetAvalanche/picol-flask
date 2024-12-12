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
        cursor.execute("INSERT INTO users (message) VALUES (%s)", (default_message,))
        conn.commit()
        # uid = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"message": "user added successfully"}), 201 # 201 Created , "uid": uid
    except Error as err:
        return jsonify({"error": str(err)}), 500 # 500 Internal Server Error
    
# !ユーザー情報一覧の取得
@user_bp.route('/', methods=['GET'])
def get_users():
    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users) # 200 OK
    except Error as err:
        return jsonify({"error": str(err)}), 500 # 500 Internal Server Error

# !ユーザー情報の取得
@user_bp.route('/<int:uid>', methods=['GET'])
def get_user(uid):
    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE uid = %s", (uid,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return jsonify(user) # 200 OK
        else:
            return jsonify({"error": "user not found"}), 404 # 404 Not Found
    except Error as err:
        return jsonify({"error": str(err)}), 500 # 500 Internal Server Error

# !ユーザー情報の更新
@user_bp.route('/<int:uid>', methods=['PUT'])
def update_user(uid):
    # リクエストデータの取得
    data = request.get_json()
    level = data.get('level')

    # 値なしエラー
    if not level:
        return jsonify({"error": "Missing level"}), 400
    
    # インジェクション
    if not isinstance(level, int):
        return jsonify({"error": "level must be an integer"}), 400
    
    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す

    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET level = %s WHERE uid = %s", (level, uid))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "user updated successfully"}), 200
    except Error as err:
        return jsonify({"error": str(err)}), 500

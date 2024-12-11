from flask import Blueprint, request, jsonify
import mysql.connector
from mysql.connector import Error

user_bp = Blueprint('user', __name__)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='mysql',  # ホスト名を確認
            port='3306',  # ポート番号を追加
            database='flask_db',
            user='flask_user',
            password='flask_password'
        )
        return conn
    except Error as err:
        print(f"Error: {err}")  # エラーメッセージを詳細に記録
        return jsonify({"error": str(err)}), 500

def init_db():
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return  # エラーメッセージを返す
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR(255) PRIMARY KEY,
                level INT
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Error as err:
        print(f"Error: {err}")

init_db()

# !ユーザー情報の追加
@user_bp.route('/', methods=['POST'])
def add_user():
    # リクエストデータの取得
    data = request.get_json()
    user_id = data.get('user_id')
    level = data.get('level')

    # 値なしエラー
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400 # 400 Bad Request
    elif not level:
        return jsonify({"error": "Missing level"}), 400 # 400 Bad Request

    # インジェクション
    if not user_id.isalnum():
        return jsonify({"error": "user_id must be alphanumeric"}), 400 # 400 Bad Request
    elif not isinstance(level, int):
        return jsonify({"error": "level must be an integer"}), 400 # 400 Bad Request

    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id, level) VALUES (%s, %s)", (user_id, level))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "user added successfully"}), 201 # 201 Created
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
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
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
@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
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
        cursor.execute("UPDATE users SET level = %s WHERE user_id = %s", (level, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "user updated successfully"}), 200
    except Error as err:
        return jsonify({"error": str(err)}), 500

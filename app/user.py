
from flask import Blueprint, request, jsonify
import mysql.connector

user_bp = Blueprint('user', __name__)

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
    if not isinstance(user_id, int):
        return jsonify({"error": "user_id must be an integer"}), 400 # 400 Bad Request
    elif not isinstance(level, int):
        return jsonify({"error": "level must be an integer"}), 400 # 400 Bad Request

    # データベースへの接続
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='flask_db',
            user='flask_user',
            password='flask_password'
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id, level) VALUES (%s, %s)", (user_id, level))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User added successfully"}), 201 # 201 Created
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500 # 500 Internal Server Error

# !ユーザー情報の取得
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # データベースへの接続
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='flask_db',
            user='flask_user',
            password='flask_password'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return jsonify(user) # 200 OK
        else:
            return jsonify({"error": "User not found"}), 404 # 404 Not Found
    except mysql.connector.Error as err:
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
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='flask_db',
            user='flask_user',
            password='flask_password'
        )
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET level = %s WHERE user_id = %s", (level, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

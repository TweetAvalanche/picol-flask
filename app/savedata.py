from flask import Blueprint, request, jsonify
import mysql.connector
from mysql.connector import Error

savedata_bp = Blueprint('savedata', __name__)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='flask_db',
            user='flask_user',
            password='flask_password'
        )
        return conn
    except Error as err:
        return jsonify({"error": str(err)}), 500

# !ユーザー情報の追加
@savedata_bp.route('/', methods=['POST'])
def add_savedata():
    # リクエストデータの取得
    data = request.get_json()
    savedata_id = data.get('savedata_id')
    level = data.get('level')

    # 値なしエラー
    if not savedata_id:
        return jsonify({"error": "Missing savedata_id"}), 400 # 400 Bad Request
    elif not level:
        return jsonify({"error": "Missing level"}), 400 # 400 Bad Request

    # インジェクション
    if not savedata_id.isalnum():
        return jsonify({"error": "savedata_id must be alphanumeric"}), 400 # 400 Bad Request
    elif not isinstance(level, int):
        return jsonify({"error": "level must be an integer"}), 400 # 400 Bad Request

    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO savedatas (savedata_id, level) VALUES (%s, %s)", (savedata_id, level))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "savedata added successfully"}), 201 # 201 Created
    except Error as err:
        return jsonify({"error": str(err)}), 500 # 500 Internal Server Error

# !ユーザー情報の取得
@savedata_bp.route('/<int:savedata_id>', methods=['GET'])
def get_savedata(savedata_id):
    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM savedatas WHERE savedata_id = %s", (savedata_id,))
        savedata = cursor.fetchone()
        cursor.close()
        conn.close()
        if savedata:
            return jsonify(savedata) # 200 OK
        else:
            return jsonify({"error": "savedata not found"}), 404 # 404 Not Found
    except Error as err:
        return jsonify({"error": str(err)}), 500 # 500 Internal Server Error

# !ユーザー情報の更新
@savedata_bp.route('/<int:savedata_id>', methods=['PUT'])
def update_savedata(savedata_id):
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
        cursor.execute("UPDATE savedatas SET level = %s WHERE savedata_id = %s", (level, savedata_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "savedata updated successfully"}), 200
    except Error as err:
        return jsonify({"error": str(err)}), 500

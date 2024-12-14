from flask import Blueprint, request, jsonify
from mysql.connector import Error
from .mysql import get_db_connection
from .character import get_character

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
            "character_name": "",
            "character_param": "",
            "character_aura_image": ""
        }
        print(response)  # レスポンスをコンソールに出力
        return jsonify(response), 201
    except Error as err:
        error_response = {"error": str(err)}
        print(error_response)  # エラーレスポンスをコンソールに出力
        return jsonify(error_response), 500

# !ユーザー情報の取得
@user_bp.route('/', methods=['GET'])
def get_user(uid = None):
    
    # パラメータの取得
    if uid is None:
        uid = request.args.get('uid', type=int)

    # 値なしエラー
    if not uid:
        error_response = {"error": "Missing uid"}
        print(error_response)  # エラーレスポンスをコンソールに出力
        return jsonify(error_response), 400
    
    # 型検証
    if not isinstance(uid, int):
        error_response = {"error": "uid must be an integer"}
        print(error_response)
        return jsonify(error_response), 400

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
                    "character_aura_image": ""
                }
                print(response)  # レスポンスをコンソールに出力
                return jsonify(response), 200
            else:
                character = get_character(cid)
                response = {
                    "uid": uid,
                    "user_message": user['message'],
                    "cid": cid,
                    "character_name": character['character_name'],
                    "character_param": character['character_param'],
                    "character_aura_image": character['character_aura_image']
                }
                print(response)  # レスポンスをコンソールに出力
                return jsonify(response), 200
        else:
            error_response = {"error": "user not found"}
            print(error_response)  # エラーレスポンスをコンソールに出力
            return jsonify(error_response), 404
    except Error as err:
        error_response = {"error": str(err)}
        print(error_response)
        return jsonify(error_response), 500

# !ユーザー情報の更新
@user_bp.route('/message', methods=['PUT'])
def update_user():
    # パラメータの取得
    uid = request.args.get('uid', type=int)
    message = request.args.get('message', type=str)

    # 値なしエラー
    if not uid:
        error_response = {"error": "Missing uid"}
        print(error_response)
        return jsonify(error_response), 400
    if not message:
        error_response = {"error": "Missing message"}
        print(error_response)
        return jsonify(error_response), 400
    
    # 型検証
    if not isinstance(uid, int):
        error_response = {"error": "uid must be an integer"}
        print(error_response)
        return jsonify(error_response), 400

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
        user = get_user(uid)
        cid = user['default_cid']
        if cid == 0:
            response = {
                "uid": uid,
                "user_message": user['message'],
                "cid": 0,
                "character_name": "",
                "character_param": "",
                "character_aura_image": ""
            }
            print(response)  # レスポンスをコンソールに出力
            return jsonify(response), 200
        else:
            character = get_character(cid)
            response = {
                "uid": uid,
                "user_message": user['message'],
                "cid": cid,
                "character_name": character['character_name'],
                "character_param": character['character_param'],
                "character_aura_image": character['character_aura_image']
            }
            print(response)  # レスポンスをコンソールに出力
            return jsonify(response), 200
    except Error as err:
        error_response = {"error": str(err)}
        print(error_response)
        return jsonify(error_response), 500

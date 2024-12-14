from flask import Blueprint, request, jsonify
from mysql.connector import Error
from .mysql import get_db_connection
from .functions.user import get_user_function, update_user_function

user_bp = Blueprint('user', __name__)

# !ユーザー情報の追加
@user_bp.route('/', methods=['POST'])
def add_user():
    # デフォルトメッセージ
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
        print(response)
        return jsonify(response), 201
    except Error as err:
        error_response = {"error": str(err)}
        print(error_response)
        return jsonify(error_response), 500

# !ユーザー情報の取得
@user_bp.route('/', methods=['GET'])
def get_user():
    # パラメータの取得
    uid = request.args.get('uid', type=int)

    response = get_user_function(uid)
    
    if "status" in response:
        status_code = response['status']
        del response["status"]    

        if status_code == 200:
            return jsonify(response), 200
        elif status_code == 400:
            return jsonify(response), 400
        elif status_code == 404:
            return jsonify(response), 404
        else:
            return jsonify(response), 500
    else:
        return jsonify(response), 500


# !ユーザー情報の更新
@user_bp.route('/message', methods=['PUT'])
def update_user():
    # パラメータの取得
    uid = request.args.get('uid', type=int)
    message = request.args.get('message', type=str)
    
    response = update_user_function(uid, message)
    
    if "status" in response:
        status_code = response['status']
        del response["status"]    

        if status_code == 200:
            return jsonify(response), 200
        elif status_code == 400:
            return jsonify(response), 400
        elif status_code == 404:
            return jsonify(response), 404
        else:
            return jsonify(response), 500
    else:
        return jsonify(response), 500


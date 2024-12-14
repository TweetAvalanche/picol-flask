from flask import Blueprint, request, jsonify
from mysql.connector import Error
import base64
from .mysql import get_db_connection
from .character_defs import generate_character

character_bp = Blueprint('character', __name__)

# !ユーザーメッセージの取得
def get_user_message(uid):
    
    # 値なしエラー
    if not uid:
        error_response = {"error": "Missing uid"}
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
        return None  # エラーメッセージを返す

    try:
        cursor = conn.cursor()
        # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
        cursor.execute("SELECT message FROM users WHERE uid = %s", (uid,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return result[0]
        else:
            return None
    except Error as err:
        return None

# !キャラクターの追加
@character_bp.route("/", methods=["POST"])
def add_character():

    # 画像が含まれているか確認、含まれていれば変換
    if 'image' not in request.files:
        return 'No image part in the request', 400

    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400

    raw_image = base64.b64encode(file.read()).decode('utf-8')
    
    # ファイルポインタを先頭にリセット
    file.seek(0)
    
    # デバッグ用のログ出力を追加
    print(f"raw_image: {raw_image[:100]}...")  # 画像データの最初の100文字を表示

    print(type(file))
    print(file)

    character = generate_character(file)

    # パラメータの取得
    uid = request.args.get('uid', type=int)
    character_param = character["character_param"]
    character_name = "NOT_IMPLEMENTED"
    character_aura_image = character["character_aura_image"]

    # 値なしエラー
    if not uid:
        error_response = {"error": "Missing uid"}
        print(error_response)
        return jsonify(error_response), 400
    if not character_param:
        error_response = {"error": "Missing character_param"}
        print(error_response)
        return jsonify(error_response), 400
    if not character_name:
        error_response = {"error": "Missing character_name"}
        print(error_response)
        return jsonify(error_response), 400
    if not character_aura_image:
        error_response = {"error": "Missing character_aura_image"}
        print(error_response)
        return jsonify(error_response), 400
    if not raw_image:
        error_response = {"error": "Missing raw_image"}
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
        cursor.execute("""
            INSERT INTO characters (uid, character_param, character_name, raw_image)
            VALUES (%s, %s, %s, %s)
        """, (uid, character_param, character_name, raw_image))
        conn.commit()
        cid = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"cid: {cid}")
        set_default_character(cid)
        response = {
            "uid": uid,
            "user_message": get_user_message(uid),
            "cid": cid,
            "character_name": character_name,
            "character_param": character_param,
            "character_aura_image": character_aura_image
        }
        print(response)  # レスポンスをコンソールに出力
        return jsonify(response), 200
    except Error as err:
        error_response = {"error": str(err)}
        print(error_response)
        return jsonify(error_response), 500

# !キャラクターの取得
@character_bp.route("/", methods=["GET"])
def get_character(cid = None):

    # パラメータの取得
    if cid is None:
        cid = request.args.get('cid', type=int)
    
    # 値なしエラー
    if not cid:
        error_response = {"error": "Missing cid"}
        print(error_response)
        return jsonify(error_response), 400
    
    # 型検証
    if not isinstance(cid, int):
        error_response = {"error": "cid must be an integer"}
        print(error_response)
        return jsonify(error_response), 400
    
    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn # エラーメッセージを返す
    
    try:
        cursor = conn.cursor(dictionary=True)
        # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
        cursor.execute("SELECT * FROM characters WHERE cid = %s", (cid,))
        character = cursor.fetchone()
        cursor.close()
        conn.close()
        if character:
            uid = character["uid"]
            response = {
                "uid": uid,
                "user_message": get_user_message(uid),
                "cid": cid,
                "character_param": character["character_param"],
                "character_name": character["character_name"],
                "character_aura_image": character["character_aura_image"],
                "raw_image": character["raw_image"]
            }
            print(response)  # レスポンスをコンソールに出力
            return jsonify(response), 200
        else:
            error_response = {"error": "character not found"}
            print(error_response)
            return jsonify(error_response), 404
    except Error as err:
        error_response = {"error": str(err)}
        print(error_response)
        return jsonify(error_response), 500

# !全キャラクターの取得
@character_bp.route("/all", methods=["GET"])
def get_all_characters():
    
    # パラメータの取得
    uid = request.args.get('uid', type=int)

    # 値なしエラー
    if not uid:
        error_response = {"error": "Missing uid"}
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
        return conn
    
    try:
        cursor = conn.cursor(dictionary=True)
        # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
        cursor.execute("SELECT * FROM characters WHERE uid = %s", (uid,))
        characters = cursor.fetchall()
        cursor.close()
        conn.close()
        response = []
        for character in characters:
            uid = character["uid"]
            response.append({
                "uid": uid,
                "user_message": get_user_message(uid),
                "cid": character["cid"],
                "character_param": character["character_param"],
                "character_name": character["character_name"],
                "character_aura_image": character["character_aura_image"],
            })
        print(response)  # レスポンスをコンソールに出力
        return jsonify(response), 200
    except Error as err:
        error_response = {"error": str(err)}
        print(error_response)
        return jsonify(error_response), 500

# !キャラクターのリネーム
@character_bp.route("/rename", methods=["PUT"])
def rename_character():

    # パラメータの取得
    cid = request.args.get('cid', type=int)
    character_name = request.args.get('character_name', type=str)
    make_default = request.args.get('make_default', type=int)

    # 値なしエラー
    if not cid:
        error_response = {"error": "Missing cid"}
        print(error_response)
        return jsonify(error_response), 400
    if not character_name:
        error_response = {"error": "Missing character_name"}
        print(error_response)
        return jsonify(error_response), 400

    # 型検証
    if not isinstance(cid, int):
        error_response = {"error": "cid must be an integer"}
        print(error_response)
        return jsonify(error_response), 400

    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す

    try:
        cursor = conn.cursor()
        # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
        cursor.execute("""
            UPDATE characters
            SET character_name = %s
            WHERE cid = %s
        """, (character_name, cid))
        conn.commit()
        cursor.close()
        conn.close()
        if make_default:
            return set_default_character(cid)
        else:
            response = get_character(cid)
            del response["raw_image"]
            print(response)  # レスポンスをコンソールに出力
            return jsonify(response), 200
    except Error as err:
        error_response = {"error": str(err)}
        print(error_response)
        return jsonify(error_response), 500

# !デフォルトキャラクターの設定
@character_bp.route("/default", methods=["PUT"])
def set_default_character(cid = None):

    uid = 0
    cid = 0

    if cid is None:
        # パラメータの取得
        uid = request.args.get('uid', type=int)
        cid = request.args.get('cid', type=int)
    else:
        character = get_character(cid)
        uid = character["uid"]

    # 値なしエラー
    if not uid:
        error_response = {"error": "Missing uid"}
        print(error_response)
        return jsonify(error_response), 400
    if not cid:
        error_response = {"error": "Missing cid"}
        print(error_response)
        return jsonify(error_response), 400

    # 型検証
    if not isinstance(uid, int):
        error_response = {"error": "uid must be an integer"}
        print(error_response)
        return jsonify(error_response), 400
    if not isinstance(cid, int):
        error_response = {"error": "cid must be an integer"}
        print(error_response)
        return jsonify(error_response), 400

    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す

    try:
        cursor = conn.cursor()
        # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
        cursor.execute("""
            UPDATE users
            SET default_cid = %s
            WHERE uid = %s
        """, (cid, uid))
        conn.commit()
        cursor.close()
        conn.close()
        response = get_character(cid)
        print(response)  # レスポンスをコンソールに出力
        del response["raw_image"]
        return jsonify(response), 200
    except Error as err:
        error_response = {"error": str(err)}
        print(error_response)
        return jsonify(error_response), 500

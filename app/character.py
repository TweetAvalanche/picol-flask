from flask import Blueprint, request, jsonify
from mysql.connector import Error
import base64
from .mysql import get_db_connection
from .character_defs import generate_character

character_bp = Blueprint('character', __name__)

# 写真から得たパラメータを返す

@character_bp.route("/", methods=["POST"])
def add_character():

    # 画像が含まれているか確認
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    file = request.files['image']
    character = generate_character(file)

    # パラメータの取得
    uid = request.args.get('uid', type=int)
    character_param = character["character_param"]
    character_name = "NOT_IMPLEMENTED"
    character_aura_image = character["character_aura_image"]
    raw_image = base64.b64encode(file.read()).decode('utf-8')

    # 値なしエラー
    if not uid:
        return jsonify({"error": "Missing uid"}), 400
    if not character_param:
        return jsonify({"error": "Missing character_param"}), 400
    if not character_name:
        return jsonify({"error": "Missing character_name"}), 400
    if not character_aura_image:
        return jsonify({"error": "Missing character_aura_image"}), 400
    if not raw_image:
        return jsonify({"error": "Missing raw_image"}), 400

    # SQLインジェクション対策
    if ";" in uid or "--" in uid or "'" in uid or "\"" in uid:
        return jsonify({"error": "Invalid characters in uid"}), 400
    if ";" in character_param or "--" in character_param or "'" in character_param or "\"" in character_param:
        return jsonify({"error": "Invalid characters in character_param"}), 400
    if ";" in character_name or "--" in character_name or "'" in character_name or "\"" in character_name:
        return jsonify({"error": "Invalid characters in character_name"}), 400
    if ";" in character_aura_image or "--" in character_aura_image or "'" in character_aura_image or "\"" in character_aura_image:
        return jsonify({"error": "Invalid characters in character_aura_image"}), 400
    if ";" in raw_image or "--" in raw_image or "'" in raw_image or "\"" in raw_image:
        return jsonify({"error": "Invalid characters in raw_image"}), 400

    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO characters (uid, character_param, character_name, raw_image)
            VALUES (%s, %s, %s, %s)
        """, (uid, character_param, character_name, raw_image))
        conn.commit()
        cid = cursor.lastrowid
        cursor.close()
        conn.close()
        response = {
            "cid": cid,
            "uid": uid,
            "character_param": character_param,
            "character_name": character_name,
            "character_aura_image": character_aura_image
        }
        return jsonify(response), 200
    except Error as err:
        return jsonify({"error": str(err)}), 500

@character_bp.route("/", methods=["GET"])
def get_character(cid = None):
    
    # パラメータの取得
    if cid is None:
        cid = request.args.get('cid', type=int)

    # 値なしエラー
    if not cid:
        return jsonify({"error": "Missing cid"}), 400
    
    # 型検証
    if not isinstance(cid, int):
        return jsonify({"error": "cid must be an integer"}), 400
    
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
            response = {
                "cid": cid,
                "uid": character["uid"],
                "character_param": character["character_param"],
                "character_name": character["character_name"],
                "raw_image": character["raw_image"]
            }
            return jsonify(response), 200
        else:
            return jsonify({"error": "character not found"}), 404
    except Error as err:
        return jsonify({"error": str(err)}), 500

@character_bp.route("/all", methods=["GET"])
def get_all_characters():
    
    # パラメータの取得
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
        return conn
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM characters WHERE uid = %s", (uid,))
        characters = cursor.fetchall()
        cursor.close()
        conn.close()
        response = []
        for character in characters:
            response.append({
                "cid": character["cid"],
                "uid": character["uid"],
                "character_param": character["character_param"],
                "character_name": character["character_name"],
                "raw_image": character["raw_image"]
            })
        return jsonify(response), 200
    except Error as err:
        return jsonify({"error": str(err)}), 500

@character_bp.route("/", methods=["PUT"])
def rename_character():

    # パラメータの取得
    cid = request.args.get('cid', type=int)
    character_name = request.args.get('character_name', type=str)

    # 値なしエラー
    if not cid:
        return jsonify({"error": "Missing cid"}), 400
    if not character_name:
        return jsonify({"error": "Missing character_name"}), 400

    # 型検証
    if not isinstance(cid, int):
        return jsonify({"error": "cid must be an integer"}), 400

    # SQLインジェクション対策
    if ";" in character_name or "--" in character_name or "'" in character_name or "\"" in character_name:
        return jsonify({"error": "Invalid characters in character_name"}), 400

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
        response = get_character(cid)
        return jsonify(response), 200
    except Error as err:
        return jsonify({"error": str(err)}), 500

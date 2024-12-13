from flask import Blueprint, request, jsonify
from mysql.connector import Error
from .mysql import get_db_connection

def add_character(uid, character_param, character_name, raw_image):

    # 値なしエラー
    if not uid:
        return jsonify({"error": "Missing uid"}), 400
    if not character_param:
        return jsonify({"error": "Missing character_param"}), 400
    if not character_name:
        return jsonify({"error": "Missing character_name"}), 400
    if not raw_image:
        return jsonify({"error": "Missing raw_image"}), 400

    # SQLインジェクション対策
    if ";" in uid or "--" in uid or "'" in uid or "\"" in uid:
        return jsonify({"error": "Invalid characters in uid"}), 400
    if ";" in character_param or "--" in character_param or "'" in character_param or "\"" in character_param:
        return jsonify({"error": "Invalid characters in character_param"}), 400
    if ";" in character_name or "--" in character_name or "'" in character_name or "\"" in character_name:
        return jsonify({"error": "Invalid characters in character_name"}), 400
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
        return jsonify({"cid": cid,"uid": uid, "character_param": character_param, "character_name": character_name}), 200
    except Error as err:
        return jsonify({"error": str(err)}), 500

def get_character(cid):

    # 値なしエラー
    if not cid:
        return jsonify({"error": "Missing cid"}), 400
    
    # 型検証
    if not isinstance(cid, int):
        return jsonify({"error": "cid must be an integer"}), 400

    # データベースへの接続
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す

    try:
        cursor = conn.cursor(dictionary=True)
        # パラメータをタプルとして渡すことで、SQLインジェクションを防ぐ
        cursor.execute("SELECT * FROM characters WHERE cid = %s", (cid,))
        character = cursor.fetchone()
        cursor.close()
        conn.close()
        if character:
            return jsonify({"cid": cid,"uid": character["uid"], "character_param": character["character_param"], "character_name": character["character_name"], "raw_image": character["raw_image"]}), 200
        else:
            return jsonify({"error": "character not found"}), 404
    except Error as err:
        return jsonify({"error": str(err)}), 500

def rename_character(cid, character_name):

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
        return jsonify({"cid": cid, "character_name": character_name}), 200
    except Error as err:
        return jsonify({"error": str(err)}), 500

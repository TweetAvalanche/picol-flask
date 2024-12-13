from flask import jsonify
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='mysql',
            port='3306',
            database='flask_db',
            user='flask_user',
            password='flask_password'
        )
        return conn
    except Error as err:
        print(f"Error: {err}")  # エラーメッセージを詳細に記録
        return jsonify({"error": str(err)}), 500

def init_users():
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                uid INT AUTO_INCREMENT PRIMARY KEY,
                message VARCHAR(512),
                default_cid INT,
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Error as err:
        print(f"Error: {err}")
        return  jsonify({"error": str(err)}), 500

def init_characters():
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                cid INT AUTO_INCREMENT PRIMARY KEY,
                uid INT,
                character_param VARCHAR(16),
                character_name VARCHAR(255),
                raw_image MEDIUMBLOB
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Error as err:
        print(f"Error: {err}")
        return jsonify({"error": str(err)}), 500

def init_tokens():
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tokens (
                token VARCHAR(6) PRIMARY KEY,
                uid INT,
                expire_at TIMESTAMP,
                is_valid BOOLEAN DEFAULT TRUE
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Error as err:
        print(f"Error: {err}")
        return jsonify({"error": str(err)}), 500

def init_db():
    result = init_users()
    if isinstance(result, tuple):
        return result  # エラーメッセージを返す

    result = init_characters()
    if isinstance(result, tuple):
        return result  # エラーメッセージを返す

    result = init_tokens()
    if isinstance(result, tuple):
        return result  # エラーメッセージを返す
    
    return jsonify({"message": "Database initialized"}), 200

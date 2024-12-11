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

def init_users(): # TODO:書き換える
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                uid INT AUTO_INCREMENT PRIMARY KEY,
                level INT
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Error as err:
        print(f"Error: {err}")
        return  jsonify({"error": str(err)}), 500

def init_charas():
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS charas (
                chara_id VARCHAR(255) PRIMARY KEY,
                level INT
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Error as err:
        print(f"Error: {err}")
        return jsonify({"error": str(err)}), 500

def init_tokens(): # TODO:書き換える
    conn = get_db_connection()
    if isinstance(conn, tuple):
        return conn  # エラーメッセージを返す
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tokens (
                token VARCHAR(255) PRIMARY KEY,
                uid INT
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

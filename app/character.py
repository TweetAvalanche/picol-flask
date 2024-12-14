from flask import Blueprint, request, jsonify
from mysql.connector import Error
import base64
from .mysql import get_db_connection
from .character_defs import generate_character
from functions import character
from functions.character import get_user_message, add_character_function, get_character_function, rename_character_function, set_default_character_function
import json

character_bp = Blueprint('character', __name__)

# !キャラクターの追加
@character_bp.route("/", methods=["POST"])
def add_character():

    # 画像が含まれているか確認、含まれていれば変換
    if 'image' not in request.files:
        return 'No image part in the request', 400

    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400

    uid = request.args.get('uid', type=int)
    
    # パラメータの取得
    response = add_character_function(file, uid)
    
    return jsonify(response), 200

# !キャラクターの取得
@character_bp.route("/", methods=["GET"])
def get_character(cid = None):

    # パラメータの取得
    if cid is None:
        cid = request.args.get('cid', type=int)
    
    response = get_character_function(cid)
    return jsonify(response), 200

# !全キャラクターの取得
@character_bp.route("/all", methods=["GET"])
def get_all_characters():

    # パラメータの取得
    uid = request.args.get('uid', type=int)



# !キャラクターのリネーム
@character_bp.route("/rename", methods=["PUT"])
def rename_character():

    # パラメータの取得
    cid = request.args.get('cid', type=int)
    character_name = request.args.get('character_name', type=str)
    make_default = request.args.get('make_default', type=int)
    
    response = rename_character_function(cid, character_name, make_default)

# !デフォルトキャラクターの設定
@character_bp.route("/default", methods=["PUT"])
def set_default_character(cid = None):
    if cid is None:
        # パラメータの取得
        uid = request.args.get('uid', type=int)
        cid = request.args.get('cid', type=int)
    else:
        character = get_character(cid)
        character = json.loads(character)
        uid = character["uid"]
        
    response = set_default_character_function(cid, uid)
    return jsonify(response), 200
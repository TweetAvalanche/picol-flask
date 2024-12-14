from flask import Blueprint, request, jsonify
from functions.character import add_character_function, get_all_characters_function, get_character_function, rename_character_function, set_default_character_function
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
        return jsonify({"error": "no selected file"}), 400

    uid = request.args.get('uid', type=int)
    
    # パラメータの取得
    response = add_character_function(file, uid)
    
    if response['status'] == 200:
        return jsonify(response), 200
    elif response['status'] == 400:
        return jsonify(response), 400
    elif response['status'] == 404:
        return jsonify(response), 404
    else:
        return jsonify(response), 500

# !キャラクターの取得
@character_bp.route("/", methods=["GET"])
def get_character():

    # パラメータの取得
    cid = request.args.get('cid', type=int)
    
    response = get_character_function(cid)
    
    if response['status'] == 200:
        return jsonify(response), 200
    elif response['status'] == 400:
        return jsonify(response), 400
    elif response['status'] == 404:
        return jsonify(response), 404
    else:
        return jsonify(response), 500

# !全キャラクターの取得
@character_bp.route("/all", methods=["GET"])
def get_all_characters():
    
    # パラメータの取得
    uid = request.args.get('uid', type=int)

    response = get_all_characters_function(uid)
    
    if response['status'] == 200:
        return jsonify(response), 200
    elif response['status'] == 400:
        return jsonify(response), 400
    elif response['status'] == 404:
        return jsonify(response), 404
    else:
        return jsonify(response), 500



# !キャラクターのリネーム
@character_bp.route("/rename", methods=["PUT"])
def rename_character():

    # パラメータの取得
    cid = request.args.get('cid', type=int)
    character_name = request.args.get('character_name', type=str)
    make_default = request.args.get('make_default', type=int)
    
    if make_default is None:
        make_default = False
    
    response = rename_character_function(cid, character_name, make_default)
    
    if response['status'] == 200:
        return jsonify(response), 200
    elif response['status'] == 400:
        return jsonify(response), 400
    elif response['status'] == 404:
        return jsonify(response), 404
    else:
        return jsonify(response), 500

# !デフォルトキャラクターの設定
@character_bp.route("/default", methods=["PUT"])
def set_default_character():

    # パラメータの取得
    cid = request.args.get('cid', type=int)
        
    response = set_default_character_function(cid)
    
    if response['status'] == 200:
        return jsonify(response), 200
    elif response['status'] == 400:
        return jsonify(response), 400
    elif response['status'] == 404:
        return jsonify(response), 404
    else:
        return jsonify(response), 500

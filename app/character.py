from flask import Blueprint, request, jsonify
from .functions.character import add_character_function, get_all_characters_function, get_character_function, rename_character_function, set_default_character_function, get_character_raw_function

character_bp = Blueprint('character', __name__)

# !キャラクターの追加
@character_bp.route("/", methods=["POST"])
def add_character():
    
    print(1)

    # 画像が含まれているか確認、含まれていれば変換
    if 'image' not in request.files:
        return 'No image part in the request', 400
    
    print(2)

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "no selected file"}), 400
    
    print(3)

    uid = request.args.get('uid', type=int)
    
    print(4)
    
    # パラメータの取得
    response = add_character_function(file, uid)
    
    print(5)
    
    if "status" in response:
        status_code = response['status']
        del response["status"]    
        return jsonify(response), status_code
    else:
        return jsonify(response), 500


# !キャラクターの取得
@character_bp.route("/", methods=["GET"])
def get_character():

    # パラメータの取得
    cid = request.args.get('cid', type=int)
    
    response = get_character_function(cid)
    
    if "status" in response:
        status_code = response['status']
        del response["status"]    
        return jsonify(response), status_code
    else:
        return jsonify(response), 500


# !全キャラクターの取得
@character_bp.route("/all", methods=["GET"])
def get_all_characters():
    
    # パラメータの取得
    uid = request.args.get('uid', type=int)

    response = get_all_characters_function(uid)
    
    if "status" in response:
        status_code = response['status']
        del response["status"]    
        return jsonify(response), status_code
    else:
        return jsonify(response), 200




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
    
    if "status" in response:
        status_code = response['status']
        del response["status"]    
        return jsonify(response), status_code
    else:
        return jsonify(response), 500


# !デフォルトキャラクターの設定
@character_bp.route("/default", methods=["PUT"])
def set_default_character():

    # パラメータの取得
    cid = request.args.get('cid', type=int)
        
    response = set_default_character_function(cid)
    
    if "status" in response:
        status_code = response['status']
        del response["status"]    
        return jsonify(response), status_code
    else:
        return jsonify(response), 500


@character_bp.route("/raw", methods=["GET"])
def get_character_raw():
    # パラメータの取得
    cid = request.args.get('cid', type=int)
    
    response = get_character_raw_function(cid)
    
    if "status" in response:
        status_code = response['status']
        del response["status"]    
        return jsonify(response), status_code
    else:
        return jsonify(response), 500

@character_bp.route("/achieve", methods=["GET"])


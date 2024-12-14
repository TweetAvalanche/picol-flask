from flask import Blueprint, request, jsonify
from .functions.token import create_token_function, check_token_function

token_bp = Blueprint('token', __name__)

# !トークンの生成
@token_bp.route("/", methods=["POST"])
def create_token():
    # パラメータの取得
    uid = int(request.args.get('uid'))

    response = create_token_function(uid)
    
    if "status" in response:
        status_code = response['status']
        del response["status"]    
        return jsonify(response), status_code
    else:
        return jsonify(response), 500


# !トークンの検証
@token_bp.route("/", methods=["GET"])
def check_token():
    # パラメータの取得
    token = request.args.get('token')
    
    response = check_token_function(token)
    
    if "status" in response:
        status_code = response['status']
        del response["status"]    
        return jsonify(response), status_code
    else:
        return jsonify(response), 500


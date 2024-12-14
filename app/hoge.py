from flask import Blueprint, jsonify, request

hoge_bp = Blueprint('hoge', __name__)

@hoge_bp.route("/", methods=["GET"])
def hello():
    uid = request.args.get('uid', type=int)
    
    response = hoge_function(uid)
    
    return jsonify(response), 200

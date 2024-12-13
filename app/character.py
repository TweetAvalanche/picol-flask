from flask import Blueprint, request, jsonify
import base64
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





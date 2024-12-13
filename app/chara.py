from flask import Blueprint, request, jsonify
from PIL import Image, ImageStat
import cv2
import numpy as np
import io
import base64

chara_bp = Blueprint('chara', __name__)

# 画像を扱う関数

def calculate_contrast(image, resize_factor=0.5):
    image = image.resize((int(image.width * resize_factor), int(image.height * resize_factor)))
    grayscale = image.convert("L")
    stat = ImageStat.Stat(grayscale)
    contrast = stat.stddev[0] 
    return contrast

def calculate_brightness(image, resize_factor=0.5):
    image = image.resize((int(image.width * resize_factor), int(image.height * resize_factor)))
    grayscale = image.convert("L")
    stat = ImageStat.Stat(grayscale)
    brightness = stat.mean[0]
    return brightness

def calculate_ratio_high_brightness(image, resize_factor=0.5):
    image = image.resize((int(image.width * resize_factor), int(image.height * resize_factor)))
    grayscale = np.array(image.convert("L"))
    high = np.sum(grayscale >= 170)
    total = grayscale.size
    return high / total

def calculate_rgb(image, resize_factor=0.5):
    image = image.resize((int(image.width * resize_factor), int(image.height * resize_factor)))
    stat = ImageStat.Stat(image)
    red, green, blue = stat.mean[:3]
    return red, green, blue



# 写真から得たパラメータを返す

@chara_bp.route("/generate", methods=["POST"])
def generate_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    nping = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(nping, cv2.IMREAD_UNCHANGED)
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    aura = cv2.imread("app/images/aura.png", cv2.IMREAD_UNCHANGED)
    
    try: # 200 OK
        red, green, blue = calculate_rgb(pil_image)
        contrast = calculate_contrast(pil_image)
        brightness = calculate_brightness(pil_image)
        high = calculate_ratio_high_brightness(pil_image)
        green_mask = (aura[:, :, 0] == 0) & (aura[:, :, 1] == 255) & (aura[:, :, 2] == 0)
        aura_bgr = aura[:, :, :3]
        aura_bgr[green_mask] = [blue, green, red]
        _, buffer = cv2.imencode('.png', image)
        img_str = base64.b64encode(buffer).decode('utf-8')
        response = {
            "contrast": contrast,
            "brightness": brightness,
            "red": red,
            "green": green,
            "blue": blue,
            "modified_image": img_str,
        }
        
        # デフォルトの名前を決める
        # TODO: データベースにparamやrawなどを登録し、name、paramやcidとかも返す
        
        return jsonify(response)
    except Exception as e: # 500 internal server error
        return jsonify({"error": str(e)}), 500


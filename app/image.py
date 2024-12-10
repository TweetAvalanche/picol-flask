from flask import Blueprint, request, jsonify
from PIL import Image, ImageStat

image_bp = Blueprint('image', __name__)

def calculate_contrast(image):
    grayscale = image.convert("L")
    stat = ImageStat.Stat(grayscale)
    contrast = stat.stddev[0] 
    return contrast

def calculate_brightness(image):
    grayscale = image.convert("L")
    stat = ImageStat.Stat(grayscale)
    brightness = stat.mean[0]
    return brightness

def calculate_rgb(image):
    stat = ImageStat.Stat(image)
    red, green, blue = stat.mean[:3]
    return red, green, blue

@image_bp.route("/analyze", methods=["POST"])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    
    try: # 200 OK
        image = Image.open(file)
        contrast = calculate_contrast(image)
        brightness = calculate_brightness(image)
        red, green, blue = calculate_rgb(image)
        
        response = {
            "contrast": contrast,
            "brightness": brightness,
            "red": red,
            "green": green,
            "blue": blue
        }
        return jsonify(response)
    except Exception as e: # 500 internal server error
        return jsonify({"error": str(e)}), 500


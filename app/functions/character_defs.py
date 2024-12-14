from PIL import Image, ImageStat
import cv2
import numpy as np
import base64


def calculate_contrast(image, resize_factor=0.5):
    image = image.resize(
        (int(image.width * resize_factor), int(image.height * resize_factor))
    )
    grayscale = image.convert("L")
    stat = ImageStat.Stat(grayscale)
    contrast = stat.stddev[0]
    return contrast


def calculate_brightness(image, resize_factor=0.5):
    image = image.resize(
        (int(image.width * resize_factor), int(image.height * resize_factor))
    )
    grayscale = image.convert("L")
    stat = ImageStat.Stat(grayscale)
    brightness = stat.mean[0]
    return brightness


def calculate_high_brightness_ratio(image, resize_factor=0.5):
    image = image.resize(
        (int(image.width * resize_factor), int(image.height * resize_factor))
    )
    grayscale = np.array(image.convert("L"))
    high = np.sum(grayscale >= 170)
    total = grayscale.size
    return high / total


def calculate_rgb(image, resize_factor=0.5):
    image = image.resize(
        (int(image.width * resize_factor), int(image.height * resize_factor))
    )
    hsv = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2HSV)
    h, _, _ = cv2.split(hsv)
    h_mean = np.mean(h)
    hsv_pixel = np.uint8([[[h_mean, 255, 255]]])
    bgr = cv2.cvtColor(hsv_pixel, cv2.COLOR_HSV2BGR)
    blue, green, red = bgr[0][0]
    return red, green, blue


def calculate_base_id(red, green, blue, brightness, ratio_high_brightness) -> int:
    is_high_red = True if red >= 100 else False
    is_high_green = True if green >= 100 else False
    is_high_blue = True if blue >= 100 else False
    is_high_ratio_high_brightness = True if ratio_high_brightness >= 0.3 else False
    is_high_brightness = True if brightness >= 150 else False

    if is_high_ratio_high_brightness:
        if is_high_red and not is_high_green and not is_high_blue:
            return 1
        elif not is_high_red and is_high_green and not is_high_blue:
            return 4
        elif not is_high_red and not is_high_green and is_high_blue:
            return 5
        else:
            return 6
    else:
        if is_high_red and is_high_blue:
            return 3
        else:
            return 2


def generate_aura(aura, red, green, blue) -> str:
    green_mask = (aura[:, :, 0] == 0) & (aura[:, :, 1] == 255) & (aura[:, :, 2] == 0)
    aura_bgr = aura[:, :, :3]
    aura_bgr[green_mask] = [blue, green, red]
    _, buffer = cv2.imencode(".png", aura_bgr)
    img_str = base64.b64encode(buffer).decode("utf-8")
    return img_str


def generate_character(file):
    nping = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(nping, cv2.IMREAD_UNCHANGED)
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    aura = cv2.imread("app/images/aura.png", cv2.IMREAD_UNCHANGED)

    # contrast = calculate_contrast(pil_image)
    brightness = calculate_brightness(pil_image)
    ratio_high_brightness = calculate_high_brightness_ratio(pil_image)
    red, green, blue = calculate_rgb(pil_image)
    base_id = calculate_base_id(red, green, blue, brightness, ratio_high_brightness)

    character_param = f"{base_id}{int(red):02x}{int(green):02x}{int(blue):02x}"
    character_aura_image = generate_aura(aura, red, green, blue)
    return {
        "character_param": character_param,
        "character_aura_image": character_aura_image,
    }

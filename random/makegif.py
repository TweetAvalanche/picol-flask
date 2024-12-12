import cv2
import numpy as np
from PIL import Image
import os

# 適当に動くgifを作るファイルです、そこそこ雑な気がする

def color_character_lineart(lineart_path, output_path, scale_factor=2):
    # キャラクターの線画を読み込む
    lineart = cv2.imread(lineart_path, cv2.IMREAD_GRAYSCALE)
    if lineart is None:
        raise FileNotFoundError(f"Lineart file '{lineart_path}' not found.")
    
    # 解像度を上げるためにリサイズ
    lineart = cv2.resize(lineart, (lineart.shape[1] * scale_factor, lineart.shape[0] * scale_factor), interpolation=cv2.INTER_CUBIC)

    # 塗り絵用の空白の画像を生成（背景を白で初期化）
    colored_image = np.full((lineart.shape[0], lineart.shape[1], 3), 255, dtype=np.uint8)

    # 線画の黒い線の内側の白い部分を塗りつぶすためのマスク作成
    # 白い部分を検出（黒い線で囲まれた内側）
    _, binary_mask = cv2.threshold(lineart, 240, 255, cv2.THRESH_BINARY_INV)
    binary_mask = cv2.erode(binary_mask, np.ones((2, 2), np.uint8), iterations=10)  # カーネルサイズを小さくして収縮
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 塗り絵のように黒い線の内側だけを青 (0000FF) で塗りつぶす
    color = (165, 150, 100)  # OpenCVはBGR形式なので青は(255, 0, 0)
    for contour in contours:
        cv2.drawContours(colored_image, [contour], -1, color, thickness=cv2.FILLED)

    # 線画の黒い線を残す（元の線画を重ねる）
    black_line_mask = (lineart < 50)  # 黒い線を検出
    colored_image[black_line_mask] = [0, 0, 0]  # 黒に設定

    # 出力画像を保存
    cv2.imwrite("temp_colored_image.png", colored_image)

    # GIFアニメーションを作成
    base_image = Image.open("temp_colored_image.png")
    frames = []
    positions = [0.02, 0, -0.02, 0]  # yの位置の割合

    for pos in positions:
        frame = Image.new("RGB", base_image.size, (255, 255, 255))
        y_offset = int(base_image.height * pos)
        frame.paste(base_image, (0, y_offset))
        frames.append(frame)

    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=500, loop=0)

if __name__ == "__main__":
    # 入力線画ファイルと出力先を指定
    lineart_path = "lineart.png"  # 線画ファイルのパス
    output_path = "colored_character.gif"  # 出力をGIFに変更
    scale_factor = 2  # 解像度を上げる

    try:
        color_character_lineart(lineart_path, output_path, scale_factor)
        print(f"塗りつぶし画像が保存されました: {output_path}")
        os.remove("temp_colored_image.png")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"エラーが発生しました: {e}")

from flask import Flask
from .mysql import init_db

def create_app():
    app = Flask(__name__)

    # ブループリントの登録
    from .root import root_bp
    from .image import image_bp
    from .user import user_bp
    from .chara import chara_bp
    app.register_blueprint(root_bp, url_prefix="/")
    app.register_blueprint(image_bp, url_prefix="/image")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(chara_bp, url_prefix="/chara")

    init_db()

    return app

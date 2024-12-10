from flask import Flask

def create_app():
    app = Flask(__name__)

    # ブループリントの登録
    from .root import root_bp
    from .image import image_bp
    app.register_blueprint(root_bp, url_prefix="/")
    app.register_blueprint(image_bp, url_prefix="/image")

    return app

from flask import Flask
from .mysql import init_db

def create_app():
    app = Flask(__name__)

    # ブループリントの登録
    from .root import root_bp
    from .user import user_bp
    from .chara import chara_bp
    from .token import token_bp

    app.register_blueprint(root_bp, url_prefix="/")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(chara_bp, url_prefix="/chara")
    app.register_blueprint(token_bp, url_prefix="/token")

    init_db()

    return app

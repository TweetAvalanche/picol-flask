from flask import Flask
from .mysql import init_db

def create_app():
    app = Flask(__name__)

    # ブループリントの登録
    from .root import root_bp
    from .user import user_bp
    from .character import character_bp
    from .token import token_bp

    app.register_blueprint(root_bp, url_prefix="/")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(character_bp, url_prefix="/character")
    app.register_blueprint(token_bp, url_prefix="/token")

    print(init_db())

    return app

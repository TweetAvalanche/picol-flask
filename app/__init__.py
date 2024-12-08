from flask import Flask

def create_app():
    app = Flask(__name__)
    # app.config.from_object('config')  # 設定を読み込む

    # ブループリントの登録
    from .routes import main
    app.register_blueprint(main)

    return app

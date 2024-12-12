from flask import Blueprint

root_bp = Blueprint('root', __name__)

@root_bp.route("/", methods=["GET"])
def hello():
    return "Hello, picol-flask is Operational / P2HACKS 2024 #TweetAvalanche"

@root_bp.route("/health", methods=["GET"])
def health():
    return "OK"

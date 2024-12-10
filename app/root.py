from flask import Blueprint

root_bp = Blueprint('root', __name__)

@root_bp.route("/", methods=["GET"])
def hello():
    return "Hello, World!"

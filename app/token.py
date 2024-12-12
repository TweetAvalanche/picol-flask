from flask import Blueprint, request, jsonify
from mysql.connector import Error
from .mysql import get_db_connection

token_bp = Blueprint('token', __name__)

@token_bp.route("/token", methods=["GET"])
def check_token():
    return "Token is valid"

@token_bp.route("/token", methods=["POST"])
def create_token():
    return "Token is created"

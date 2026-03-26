from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    body = request.get_json()
    if not body:
        abort(400)
    user = AuthService.signup(body)
    return jsonify(user), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    if not body:
        abort(400)
    user = AuthService.login(body)
    return jsonify(user), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = AuthService.get_me(user_id)
    return jsonify(user), 200
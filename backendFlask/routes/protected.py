from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/protected')
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(message=f"Welcome {current_user} to the protected route!")
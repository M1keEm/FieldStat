from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return """
    <h1>Welcome to the Crop Yield API</h1>
    <p>Use the endpoint /crop_yield to get crop yield data.</p>
    """
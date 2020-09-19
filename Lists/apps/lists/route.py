from flask import Blueprint, request, jsonify

list_bp = Blueprint('list', __name__)

@list_bp.route('/test', methods=['GET'])
def test():
	return jsonify([{'message':'test lists'}]), 200
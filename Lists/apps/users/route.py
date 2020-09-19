from flask import Blueprint, request, jsonify

user_bp = Blueprint('user', __name__)

@user_bp.route('/test', methods=['GET'])
def test():
	return jsonify([{'message':'test users'}]), 200
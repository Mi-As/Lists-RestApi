from flask import Blueprint, request, jsonify

notes_bp = Blueprint('list', __name__)

@notes_bp.route('/test', methods=['GET'])
def test():
	return jsonify([{'message':'test lists'}]), 200
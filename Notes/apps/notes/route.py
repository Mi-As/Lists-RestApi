from flask import Blueprint, request, jsonify

notes_bp = Blueprint('note', __name__)

@notes_bp.route('/test', methods=['GET'])
def test():
	return jsonify([{'message':'test notes'}]), 200
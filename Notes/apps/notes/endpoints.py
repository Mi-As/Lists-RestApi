from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, current_user

from .services import (
	create_note, update_note, delete_note, note_to_dict, get_note_all,
	tag_to_dict, get_all_note_tags)


class Notes(MethodView):
	""" Endpoint: /notes """

	def filter_notes(self, request_args):
		"""
		Formats and passes filter arguments from request to
		get_note_all service
		:params request_args: 
		:return notes: note objects
		:return used_filters: 
		"""

		filter_avl = ['id','is_archived', 'from_date', 'till_date', 'type_name', 'tag_list']
		filter_args = dict(filter(lambda arg: arg[0] in filter_avl, request_args.items()))
		filter_args['user_public_id'] = current_user.public_id
		if 'tag_list' in filter_args and filter_args['tag_list']:
			filter_args['tag_list'] = filter_args['tag_list'].split(',')

		used_filters = list(filter_args.keys())
		notes = get_note_all(filter_args)
		return notes, used_filters	
	
	@jwt_required
	def post(self):
		"""
		creates a new note for the current user
		:params text, type, tags:
		:return: success message, note obj
		"""
		json_data = request.get_json()

		if not 'text' in json_data.keys():
			return jsonify({"msg":'A Key is missing, check: text!'}), 400

		note_data = {
			'user_public_id':current_user.public_id,
			'text':json_data['text']}

		if 'type' in json_data.keys() and json_data['type']:
			note_data['type_name'] = json_data['type']

		if 'tags' in json_data.keys() and json_data['tags']:
			note_data['tag_list'] = json_data['tags']

		new_note = create_note(**note_data)

		return jsonify(
			{"msg":'Note has been successfully created!',
			 "note": note_to_dict(new_note)}
		), 201

	@jwt_required
	def get(self):
		"""
		:params id, is_archived, from_date, till_date, type_name, tag_list: filter parameters
		:return: note data
		"""
		notes, used_filters = self.filter_notes(request.args)

		return jsonify({
			"msg": "Request was processed successfully! {} notes found.".format(len(notes)),
			"filters":used_filters,
			"notes":[note_to_dict(note) for note in notes or []]
		}), 200

	@jwt_required	
	def put(self):
		"""
		updates requested notes by parametes
		:params id, is_archived, from_date, till_date, type_name, tag_list: filter parameters
		:params text, type, tags: 
		:return: success message
		"""

		json_data = request.get_json()
		notes, used_filters = self.filter_notes(request.args)
		if not notes:
			return jsonify({"msg": 'Notes not found, please check your parameters!'}), 404

		for note in notes:
			for key, data in json_data.items():
				if key == 'text':
					note.text = data
				elif key == 'type':
					note.type_name = data
				elif key == 'tags':
					note.set_tags(data)
			update_note(note)

		return jsonify({"msg":
			'{} notes have been successfully updated!'.format(len(notes))
		}), 200

	@jwt_required
	def delete(self):
		"""
		deletes requested notes
		:params id, is_archived, from_date, till_date, type_name, tag_list: filter parameters
		:return: success message
		"""
		notes, used_filters = self.filter_notes(request.args)
		if not notes:
			return jsonify({"msg": 'Notes not found, please check your parameters!'}), 404

		for note in notes:
			delete_note(note)

		return jsonify({"msg":
			'{} notes have been successfully deleted!'.format(len(notes))
		}), 200


class Tags(MethodView):
	""" Endpoint: /notes/tags """

	def filter_tags(self, request_args):
		"""
		Formats and passes filter arguments from request to
		get_all_note_tags service
		:params request_args: 
		:return tags: tag objects
		"""
		filter_avl = ['id','name']
		filter_args = dict(filter(lambda arg: arg[0] in filter_avl, request_args.items()))
		filter_args['user_public_id'] = current_user.public_id

		tags = get_all_note_tags(filter_args)
		return tags
	
	@jwt_required
	def get(self):
		"""
		:params id, name
		:return: tag data
		"""
		tags = self.filter_tags(request.args)

		return jsonify({
			"msg": "Request was processed successfully! {} tags found.".format(len(tags)),
			"tags":[tag_to_dict(tag) for tag in tags or []]
			}), 200

	@jwt_required
	def put(self):
		"""
		renames requested tags
		:params id, name
		:return: success message
		"""
		json_data = request.get_json()
		tags = self.filter_tags(request.args)
		if not tags:
			return jsonify({"msg": 'Tags not found, please check your parameters!'}), 404

		if not 'name' in json_data.keys():
			return jsonify({"msg": 'Missing name parameter'}), 400

		for tag in tags:
			tag.name = json_data['name']

		return jsonify({"msg":
			'{} tags have been successfully renamed!'.format(len(tags))
		}), 200

	@jwt_required
	def delete(self):
		"""
		deletes requested tags
		:params id, name
		:return: success message
		"""
		tags = self.filter_tags(request.args)
		if not tags:
			return jsonify({"msg": 'Tags not found, please check your parameters!'}), 404

		for tag in tags:
			delete_note(tag)

		return jsonify({"msg":
			'{} tags have been successfully deleted!'.format(len(tags))
		}), 200

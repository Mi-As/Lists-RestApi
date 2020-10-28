from datetime import datetime

from ... import db
from ..services import except_invalid_request_error as except_error
from . import models

def delete_obj(obj):
	db.session.delete(obj)
	db.session.commit()

def update_obj(obj):
	db.session.commit()

# NOTE
@except_error
def get_note_one(filter_data):
	return models.Note.query.filter_by(**filter_data).first()

@except_error
def get_note_all(filter_data=None):

	my_query = models.Note.query
	if filter_data:

		is_in_data = lambda key: key in filter_data.keys()
		from_date = None if not is_in_data('from_date') else filter_data.pop('from_date')
		till_date = None if not is_in_data('till_date') else filter_data.pop('till_date')
		tags = None if not is_in_data('tag_list') else filter_data.pop('tag_list')
		

		my_query = my_query.filter_by(**filter_data)
		if from_date:
			my_query = my_query.filter(models.Note.last_change_time >= from_date)
		if till_date:
			my_query = my_query.filter(models.Note.last_change_time <= till_date)
		if tags:
			my_query = my_query.filter(models.Note.tags.any(models.NoteTag.name.in_(tags)))

	return my_query.all()

# todo except name unique error
def create_note(user_public_id, text, type_name='note', tag_list=[]):
	new_note = models.Note(user_public_id, type_name, tag_list, text)
	db.session.add(new_note)
	db.session.commit()

	return new_note

def update_note(note_obj):
	note_obj.last_change_time = datetime.now()
	db.session.commit()

def note_to_dict(note_obj):
	return {
		'id': note_obj.id,
		'text': note_obj.text,
		'type': note_obj.type_name,
		'tags': [t.name for t in note_obj.tags],
		'last_change_time': note_obj.last_change_time,
		'is_archived': note_obj.is_archived
	}


# NOTE TYPE
@except_error
def get_note_type(filter_data):
	return models.NoteType.query.filter_by(**filter_data).first()

@except_error
def get_all_note_types(filter_data=None):
	if filter_data:
		return models.NoteType.query.filter_by(**filter_data).all()
	return models.NoteType.query.all()


def create_type(name):
	new_type = models.NoteType(name=name)
	db.session.add(new_type)
	db.session.commit()
	return new_type

def type_to_dict(type_obj):
	return {
		'id':type_obj.id,
		'name':type_obj.name
	}

# NOTE TAG
@except_error
def get_note_tag(filter_data):
	return models.NoteTag.query.filter_by(**filter_data).first()

@except_error
def get_all_note_tags(filter_data=None):
	if filter_data:
		return models.NoteTag.query.filter_by(**filter_data).all()
	return models.NoteTag.query.all()

def create_tag(user_public_id, name):
	new_tag = models.NoteTag(user_public_id=user_public_id, name=name)
	db.session.add(new_tag)
	db.session.commit()
	return new_tag

def tag_to_dict(tag_obj):
	return {
		'id': tag_obj.id,
		'name': tag_obj.name
	}



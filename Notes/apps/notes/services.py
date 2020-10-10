from ..services import except_invalid_request_error as except_error
from . import models

# NOTE
@except_error
def get_note_one(filter_data):
	return models.Note.query.filter_by(**filter_data).first()

@except_error
def get_note_all(filter_data=None):
	if filter_data:
		return models.Note.query.filter_by(**filter_data).first()
	return models.Note.query.all()


# NOTE TYPE
def get_note_type(name):
	return models.NoteType.query.filter_by(name=name).first()

def get_all_note_types():
	return models.NoteType.query.all()

# NOTE TAG
def get_note_tag(name):
	return models.NoteTag.query.filter_by(name=name).first()

def get_all_note_tags():
	return models.NoteTag.query.all()



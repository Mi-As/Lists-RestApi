from ..apps.notes import endpoints, models
from ..apps.users.models import User

from ..apps.notes.services import get_note_tag, get_note_type, get_note_one
from ..apps.users.services import get_user_one

class TestModels:
	
	# NOTE_TAG
	def test_new_note_tag(self, db_session):
		# create tag and add to database
		tag_values = {'name':'todo'}
		db_session.add(models.NoteTag(**tag_values))
		db_session.commit()
		# get tag and test values
		new_tag = get_note_tag(name=tag_values['name'])
		assert new_tag

	# NOTE_TYPE
	def test_new_note_type(self, db_session):
		# create type and add to database
		type_values = {'name':'note'}
		db_session.add(models.NoteType(**type_values))
		db_session.commit()
		# get type and test values
		new_type = get_note_type(name=type_values['name'])
		assert new_type

	# NOTE
	def test_new_note(self, db_session, test_user):
		note_user, _ = test_user
		# create note and add to database
		note_values = {
			'user_public_id':note_user.public_id,
			'type_name':'note',  # has to already exit
			'tag_list':['todo','grocary'],
			'text':'This is a note text!'}
		note_obj = models.Note(**note_values)
		db_session.add(note_obj)
		db_session.commit()

		# get note and test values
		# public_id text last_change_time is_active user_public_id type_name tags
		new_note = get_note_one({'id':note_obj.id})
		assert new_note.public_id
		assert new_note.text == note_values['text']
		assert new_note.last_change_time
		assert new_note.is_active == True
		assert new_note.user_public_id == note_values['user_public_id']
		assert new_note.type_name == note_values['type_name']
		assert len(new_note.tags) == 2
		# test relationship to user 
		altered_note_user = get_user_one({'id':note_user.id})
		assert altered_note_user.notes[0].public_id == new_note.public_id 

class TestServices:
	
	def test_get_note_one(self):
		pass

	def test_get_note_type(self):
		pass

	def test_get_note_tag(self):
		pass

	def test_get_all_note_tags(self):
		pass

class TestEndpoints:
	pass

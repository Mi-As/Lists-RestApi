from ..apps.notes import route, models
from ..apps.users.models import User

class TestModels:
	
	def test_new_note_tag(self, db_session):
		# create tag and add to database
		tag_values = {'name':'todo'}
		db_session.add(models.NoteTag(**tag_values))
		db_session.flush()
		# get tag and test values
		new_tag = models.NoteTag.query.filter_by(id=1).first()
		assert new_tag.name == tag_values['name']


	def test_new_note_type(self, db_session):
		# create type and add to database
		type_values = {'name':'note'}
		db_session.add(models.NoteType(**type_values))
		db_session.flush()
		# get type and test values
		new_type = models.NoteType.query.filter_by(id=1).first()
		assert new_type.name == type_values['name']

	def test_new_note(self, db_session, test_user):
		note_user, _ = test_user
		db_session.add(note_user)
		# create note and add to database
		note_values = {
			'user_public_id':note_user.public_id,
			'type_name':'note',  # has to already exit
			'tag_list':['todo','grocary'],
			'text':'This is a note text!'}
		db_session.add(models.Note(**note_values))
		db_session.flush()

		# get note and test values
		# public_id text last_change_time is_active user_public_id type_name tags
		new_note = models.Note.query.filter_by(id=1).first()
		assert new_note.public_id
		assert new_note.text == note_values['text']
		assert new_note.last_change_time
		assert new_note.is_active == True
		assert new_note.user_public_id == note_values['user_public_id']
		assert new_note.type_name == note_values['type_name']
		assert len(new_note.tags) == 2
		# test relationship to user 
		altered_note_user = User.query.filter_by(id=note_user.id).first()
		assert altered_note_user.notes[0].public_id == new_note.public_id 

class TestServices:
	pass

class TestEndpoints:
	pass

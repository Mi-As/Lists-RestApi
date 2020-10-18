from ..apps.notes import endpoints, models
from ..apps.users.models import User

from ..apps.notes.services import (get_note_one, get_note_all,
	get_note_type, get_all_note_types, get_note_tag, get_all_note_tags)
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

	def test_get_note_all(self, test_user, db_session):
		note_user, _ = test_user
		note_values = {
			'user_public_id':note_user.public_id,
			'type_name':'note',  # has to already exit
			'tag_list':['todo','grocary'],
			'text':'This is a note text!'}
		note_obj = models.Note(**note_values)
		db_session.add(note_obj)
		db_session.commit()

		assert get_note_all()

		filter_data1 = {'type_name': note_values['type_name']}
		assert get_note_all(filter_data1)

		# no such value
		filter_data2 = {'type_name':'i dont exist'}
		assert not get_note_all(filter_data2)

		# key error
		filter_data3 = {'i dont exist': note_values['type_name']}
		assert not get_note_all(filter_data3)

	def test_get_note_type(self, db_session):
		type_values = {'name':'type_test1'}
		db_session.add(models.NoteType(**type_values))
		db_session.commit()

		filter1 = get_note_type(type_values['name'])
		assert filter1.name == type_values['name']

		# no such value
		assert get_note_type('i dont exist') is None

	def test_get_all_note_types(self, db_session):
		start_all = len(get_all_note_types())
		
		db_session.add(models.NoteType(name='type_test2'))
		db_session.commit()

		assert len(get_all_note_types()) == start_all + 1

	def test_get_note_tag(self, db_session):
		tag_values = {'name':'tag_test1'}
		db_session.add(models.NoteTag(**tag_values))
		db_session.commit()

		filter1 = get_note_tag(tag_values['name'])
		assert filter1.name == tag_values['name']

		# no such value
		assert get_note_tag('i dont exist') is None

	def test_get_all_note_tags(self, db_session):
		start_all = len(get_all_note_tags())
		
		db_session.add(models.NoteTag(name='tag_test2'))
		db_session.commit()

		assert len(get_all_note_tags()) == start_all + 1

class TestEndpoints:
	pass

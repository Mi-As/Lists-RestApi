from datetime import timedelta
from flask import json

from ..apps.notes import endpoints, models, services
from ..apps.users import services as user_services


url = '/notes'
url_tags = url + '/tags'

class TestModels:
	
	# NOTE_TAG
	def test_new_note_tag(self, db_session, test_user):
		note_user, _ = test_user
		# create tag and add to database
		tag_values = {'name':'todo', 'user_public_id':note_user.public_id}
		db_session.add(models.NoteTag(**tag_values))
		db_session.commit()
		# get tag and test values
		new_tag = services.get_note_tag({
			'user_public_id':note_user.public_id,
			'name':tag_values['name']})
		assert new_tag

	# NOTE_TYPE
	def test_new_note_type(self, db_session):
		# create type and add to database
		type_values = {'name':'new'}
		db_session.add(models.NoteType(**type_values))
		db_session.commit()
		# get type and test values
		new_type = services.get_note_type({'name':type_values['name']})
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
		# public_id text last_change_time is_archived user_public_id type_name tags
		new_note = services.get_note({'id':note_obj.id})
		assert new_note.public_id
		assert new_note.text == note_values['text']
		assert new_note.last_change_time
		assert new_note.is_archived == False
		assert new_note.user_public_id == note_values['user_public_id']
		assert new_note.type_name == note_values['type_name']
		assert len(new_note.tags) == 2
		# test relationship to user 
		altered_note_user = user_services.get_user({'id':note_user.id})
		assert altered_note_user.notes[0].public_id == new_note.public_id 


class TestServices:

	def test_delete_obj(self, test_user_note):
		_, _, note = test_user_note
		services.delete_obj(note)

		assert services.get_note({'id':note.id}) is None

	def test_update_obj(self, test_user_type):
		_, _, _type = test_user_type
		_type.name = 'altered'
		services.update_obj(_type)

		updated_type = services.get_note_type({'id':_type.id})
		assert updated_type.name == 'altered'

	# NOTE
	def test_get_note(self, test_user_note):
		_, _, note = test_user_note

		filter_data1 = {'id': note.id}
		filter1 = services.get_note(filter_data1)
		assert filter1.id == note.id

		# no such value
		filter_data2 = {'id': 'i dont exist'}
		assert services.get_note(filter_data2) is None

		# key error
		filter_data3 = {'i dont exist': note.id}
		assert services.get_note(filter_data3) is None

	def test_get_notes(self, test_user_note):
		note_user, _, note = test_user_note

		assert services.get_notes()

		filter_data1 = {
			'type_name': note.type_name,
			'tag_list':[note.tags[0].name],
			'from_date': note.last_change_time - timedelta(days=1),
			'till_date': note.last_change_time + timedelta(days=1)}
		assert services.get_notes(filter_data1)

		# no such value
		filter_data2 = {'id':'i dont exist'}
		assert not services.get_notes(filter_data2)

		# key error
		filter_data3 = {'i dont exist': note.id}
		assert not services.get_notes(filter_data3)

	def test_create_note(self, test_user):
		note_user, _ = test_user
		note_text = 'a very cool test text'

		new_note = services.create_note(
			user_public_id=note_user.public_id, text=note_text)

		assert new_note
		assert services.get_note({'text':note_text}) 

	def test_update_note(self, test_user_note):
		_, _, note = test_user_note
		note.text = 'altered'
		services.update_note(note)

		updated_note = services.get_note({'id':note.id}) 
		assert updated_note.text == 'altered'

	def test_note_to_dict(self, test_user_note):
		_, _, note = test_user_note
		dict_data = services.note_to_dict(note)

		assert dict_data['text'] == note.text
		assert dict_data['type'] == note.type_name
		assert len(dict_data['tags']) == len(note.tags)
		assert dict_data['last_change_time'] == note.last_change_time
		assert dict_data['is_archived'] == note.is_archived

	# NOTE_TYPE
	def test_get_note_type(self, test_user_type):
		_, _, _type = test_user_type

		filter1 = services.get_note_type({'id':_type.id})
		assert filter1.name == _type.name

		# no such value
		assert services.get_note_type({'name':'i dont exist'}) is None

	def test_get_note_types(self, test_user_type):
		_, _, _type = test_user_type
		
		note_types = services.get_note_types({
			'name':_type.name})
		assert note_types
		assert services.get_note_types()

	def test_create_note_type(self):
		new_type = services.create_type('picture')

		assert new_type
		assert services.get_note_type({'name':'picture'})

	def test_type_to_dict(self, test_user_type):
		_, _, _type = test_user_type
		dict_data = services.type_to_dict(_type)

		assert dict_data['id'] == _type.id
		assert dict_data['name'] == _type.name

	# NOTE_TAG
	def test_get_note_tag(self, test_user_tag):
		_, _, tag = test_user_tag

		filter1 = services.get_note_tag(
			{'user_public_id':tag.user_public_id,
			 'name':tag.name})
		assert filter1.name == tag.name

		# no such value
		filter2 = services.get_note_tag(
			{'user_public_id': tag.user_public_id,
			 'name':'i dont exist'})
		assert filter2 is None

	def test_get_note_tags(self, test_user_tag):
		_, _, tag = test_user_tag

		note_tags = services.get_note_tags({
			'user_public_id':tag.user_public_id})
		assert note_tags
		assert services.get_note_tags()

	def test_create_note_tag(self, test_user):
		note_user, _ = test_user

		new_tag = services.create_tag(
			user_public_id=note_user.public_id, name='games')

		assert new_tag
		assert services.get_note_tag({'name':'games'}) 

	def test_tag_to_dict(self, test_user_tag):
		_, _, tag = test_user_tag
		dict_data = services.tag_to_dict(tag)

		assert dict_data['id'] == tag.id
		assert dict_data['name'] == tag.name


class TestEndpoints:
	
	# NOTES
	def test_notes_post_request(self, client, test_user):
		user, user_data = test_user
		headers = {'Content-Type': 'application/json',
				   'Authorization': 'Bearer ' + user_data['access_token']}

		# valid data
		data1 = {'text':'note text','type':'note','tags':['todo', 'grocary']}
		response1 = client.post(url, headers=headers, data=json.dumps(data1))
		json_data1 = response1.get_json()

		assert response1.status_code == 201
		assert json_data1["msg"]
		assert json_data1["note"]["text"] == data1['text']
		assert services.get_note({'user_public_id':user.public_id})

		# invalid keys
		data2 = {'type':'note','tags':['todo', 'grocary']}
		response2 = client.post(url, headers=headers, data=json.dumps(data2))
		json_data2 = response2.get_json()

		assert response2.status_code == 400
		assert json_data2["msg"]

	def test_notes_get_request(self, client, test_user_note):
		user, user_data, note = test_user_note
		headers = {'Content-Type': 'application/json',
				   'Authorization': 'Bearer ' + user_data['access_token']}

		url_data = '?is_archived={is_archived}&from_date={from_date}&till_date={till_date}&type_name={type_name}&tag_list={tag_list}'\
			.format(
				is_archived=int(note.is_archived),
				from_date=(note.last_change_time - timedelta(days=1)).date().isoformat(),
				till_date=(note.last_change_time + timedelta(days=1)).date().isoformat(),
				type_name=note.type_name,
				tag_list=','.join([t.name for t in note.tags]))

		response = client.get(url + url_data, headers=headers)
		json_data = response.get_json()

		assert response.status_code == 200
		assert json_data["msg"]
		assert json_data["filters"]
		assert json_data["notes"][0]["id"] == note.id

	def test_notes_put_request(self, client, test_user_note):
		user, user_data, note = test_user_note
		headers = {'Content-Type': 'application/json',
				   'Authorization': 'Bearer ' + user_data['access_token']}

		url_data1 = '?id={}'.format(note.id)
		data1 = {'text':'new text', 'type':'note', 'tags':['new tag']}
		response1 = client.put(url + url_data1, headers=headers, data=json.dumps(data1))
		json_data1 = response1.get_json()

		assert response1.status_code == 200
		assert json_data1["msg"]
		updated_note = services.get_note({'id':note.id})
		assert updated_note.text == data1['text']
		assert updated_note.type_name == data1['type']
		assert updated_note.tags[0].name == data1['tags'][0]

		# invalid url data
		url_data2 = '?id={}'.format('i dont exit')
		response2 = client.put(url + url_data2, headers=headers, data=json.dumps(data1))
		json_data2 = response2.get_json()

		assert response2.status_code == 404
		assert json_data2["msg"]

	def test_notes_delete_request(self, client, test_user_note):
		user, user_data, note = test_user_note
		headers = {'Content-Type': 'application/json',
				   'Authorization': 'Bearer ' + user_data['access_token']}

		url_data1 = '?id={}'.format(note.id)
		response1 = client.delete(url + url_data1, headers=headers)
		json_data1 = response1.get_json()

		assert response1.status_code == 200
		assert json_data1["msg"]
		assert services.get_note({'id':note.id}) is None

		# invalid url data
		url_data2 = '?id={}'.format('i dont exit')
		response2 = client.delete(url + url_data2, headers=headers)
		json_data2 = response2.get_json()

		assert response2.status_code == 404
		assert json_data2["msg"]

	# TAGS
	def test_tags_get_request(self, client, test_user_tag):
		user, user_data, tag = test_user_tag
		headers = {'Content-Type': 'application/json',
				   'Authorization': 'Bearer ' + user_data['access_token']}

		url_data = '?name={name}'.format(id=tag.id, name=tag.name)
		response = client.get(url_tags + url_data, headers=headers)
		json_data = response.get_json()

		assert response.status_code == 200
		assert json_data["msg"]
		assert json_data["tags"][0]["id"] == tag.id

	def test_tags_put_request(self, client, test_user_tag):
		user, user_data, tag = test_user_tag
		headers = {'Content-Type': 'application/json',
				   'Authorization': 'Bearer ' + user_data['access_token']}

		url_data1 = '?id={}'.format(tag.id)
		data1 = {'name':'new name'}
		response1 = client.put(url_tags + url_data1, headers=headers, data=json.dumps(data1))
		json_data1 = response1.get_json()

		assert response1.status_code == 200
		assert json_data1["msg"]
		updated_tag = services.get_note_tag({'id':tag.id})
		assert updated_tag.name == data1['name']

		# invalid url data
		url_data2 = '?id={}'.format('i dont exist')
		response2 = client.put(url_tags + url_data2, headers=headers, data=json.dumps(data1))
		json_data2 = response2.get_json()

		assert response2.status_code == 404
		assert json_data2["msg"]

		# invalid key
		data3 = {'i dont exist': 'new name'}
		response3 = client.put(url_tags + url_data1, headers=headers, data=json.dumps(data3))
		json_data3 = response3.get_json()

		assert response3.status_code == 400
		assert json_data3["msg"]

	def test_tags_delete_request(self, client, test_user_tag):
		user, user_data, tag = test_user_tag
		headers = {'Content-Type': 'application/json',
				   'Authorization': 'Bearer ' + user_data['access_token']}

		url_data1 = '?id={}'.format(tag.id)
		response1 = client.delete(url_tags + url_data1, headers=headers)
		json_data1 = response1.get_json()

		assert response1.status_code == 200
		assert json_data1["msg"]
		assert services.get_note_tag({"id":tag.id}) is None

		# invalid url data
		url_data2 = '?id={}'.format('i dont exit')
		response2 = client.delete(url_tags + url_data2, headers=headers)
		json_data2 = response2.get_json()

		assert response2.status_code == 404
		assert json_data2["msg"]

	# TYPES
	def test_type_post_request(self, client, test_user_type):
		pass

	def test_type_get_request(self, client, test_user_type):
		pass

	def test_type_put_request(self, client, test_user_type):
		pass

	def test_type_delete_request(self, client, test_user_type):
		pass

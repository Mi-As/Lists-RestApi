from .endpoints import NotesEndpoints, TagsEndpoints, TypesEndpoints

def init_app(app):
	app.add_url_rule('/notes', view_func=NotesEndpoints.as_view('notes_endpoints'))
	app.add_url_rule('/notes/tags', view_func=TagsEndpoints.as_view('tags_endpoints'))
	app.add_url_rule('/notes/types', view_func=TypesEndpoints.as_view('types_endpoints'))
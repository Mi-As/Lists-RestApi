from .endpoints import NotesAPI

def init_app(app):
	app.add_url_rule('/notes', view_func=NotesAPI.as_view('notes'))
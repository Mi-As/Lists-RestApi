from .endpoints import Notes, Tags, Types

def init_app(app):
	app.add_url_rule('/notes', view_func=Notes.as_view('notes'))
	app.add_url_rule('/notes/tags', view_func=Tags.as_view('tags'))
	app.add_url_rule('/notes/types', view_func=Types.as_view('types'))
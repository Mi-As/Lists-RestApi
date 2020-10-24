from .endpoints import UserAPI


def init_app(app):
	app.add_url_rule('/user', view_func=UserAPI.as_view('user'))
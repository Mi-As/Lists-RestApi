from .endpoints import UserEndpoints


def init_app(app):
	app.add_url_rule('/user', view_func=UserEndpoints.as_view('user_endpoints'))
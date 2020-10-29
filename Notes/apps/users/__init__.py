from .endpoints import UserEndpoints, user_admin_bp


def init_app(app):
	app.add_url_rule('/user', view_func=UserEndpoints.as_view('user_endpoints'))
	app.register_blueprint(user_admin_bp, url_prefix='/user')
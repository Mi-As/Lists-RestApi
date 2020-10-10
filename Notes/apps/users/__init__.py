from .endpoints import user_bp

def init_app(app):
	app.register_blueprint(user_bp, url_prefix='/user')
from .route import list_bp

def init_app(app):
	app.register_blueprint(list_bp, url_prefix='/list')
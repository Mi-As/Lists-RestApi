from .route import notes_bp

def init_app(app):
	app.register_blueprint(notes_bp, url_prefix='/note')
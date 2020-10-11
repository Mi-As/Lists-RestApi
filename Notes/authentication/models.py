from .. import db
from datetime import datetime
from flask_jwt_extended import decode_token
from ..apps.users.services import get_user_one

# https://github.com/vimalloc/flask-jwt-extended/blob/
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    type = db.Column(db.String(10), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    # One-to-Many
    user_public_id = db.Column(db.String(50), db.ForeignKey('user.public_id', ondelete='CASCADE'))

    def __init__(self, encoded_token, user_identity):
    	decoded_token = decode_token(encoded_token)

    	self.jti = decoded_token['jti']
    	self.type = decoded_token['type']
    	self.revoked = False
    	self.expires = datetime.fromtimestamp( 
    			decoded_token['exp']) # utc to datetime
    	self.set_user_id(user_identity)

    def set_user_id(self, public_id):
    	user = get_user_one({'public_id':public_id})
    	assert user, "user has no such public id!" # 500 internal server error
    	self.user_public_id = public_id
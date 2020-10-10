from functools import wraps
import sqlalchemy

def except_invalid_request_error(func):
	@wraps(func)
	def wrapped(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except sqlalchemy.exc.InvalidRequestError:
			return None
	return wrapped
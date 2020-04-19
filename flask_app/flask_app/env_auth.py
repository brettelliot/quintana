from functools import wraps
from flask import request, abort
import os

# Require an api key to access methods with the `api_key` decorator
def require_api_key(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.args.get('api_key') and \
           request.args.get('api_key') == os.environ['API_KEY']:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function

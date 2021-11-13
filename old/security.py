from os import name
from flask import request, make_response
from functools import wraps

from flask.wrappers import Response


class WebAdminAuthentication:

    def __init__(self, admin_username: str, admin_password: str) -> None:
        self.admin_username = admin_username
        self.admin_password = admin_password

    def _authenticate(self, username: str, password: str) -> bool:
        """ Return True if user sould be permited to access """

        return username == self.admin_username and password == self.admin_password

    def auth_required(self, endpoint_function):
        """ Decorator for endpoints which require authentication. Use below `@app.route()` """
        @wraps(endpoint_function)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if auth and self._authenticate(auth.username, auth.password):
                return endpoint_function(*args, **kwargs)

            return make_response("No se pudo verificar el login!", 401, {'WWW-authenticate': 'Basic realm="Login required"'})

        return decorated

    def logout_endpoint(self, endpoint_function):
        """ Decorator for logout endpoint. Use below `@app.route()` """
        @wraps(endpoint_function)
        def decorated(*args, **kwargs):
            response: Response = endpoint_function(*args, **kwargs)
            response.headers['WWW-authenticate'] = 'Basic realm="..."'
            response.status_code = 401
            return response

        return decorated

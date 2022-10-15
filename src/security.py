from flask import request, make_response
from flask.wrappers import Response
from functools import wraps
from .config import AdminConfig

admin_config = AdminConfig()


def _authenticate(username: str, password: str) -> bool:
    """Return True if user sould be permited to access"""

    return username == admin_config.username and password == admin_config.password


def auth_required(endpoint_function):
    """Decorator for endpoints which require authentication. Use below `@app.route()`"""

    @wraps(endpoint_function)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and _authenticate(auth.username, auth.password):
            return endpoint_function(*args, **kwargs)

        return make_response(
            "No se pudo verificar el login!",
            401,
            {"WWW-authenticate": 'Basic realm="Login required"'},
        )

    return decorated


def logout_endpoint(endpoint_function):
    """Decorator for logout endpoint. Use below `@app.route()`"""

    @wraps(endpoint_function)
    def decorated(*args, **kwargs):
        response: Response = endpoint_function(*args, **kwargs)
        response.headers["WWW-authenticate"] = 'Basic realm="..."'
        response.status_code = 401
        return response

    return decorated

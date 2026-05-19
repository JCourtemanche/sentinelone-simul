from functools import wraps
from flask import request, jsonify
from config import Config


def require_api_token(f):
    """Decorator requiring SentinelOne-style API token auth.

    Accepts: Authorization: ApiToken <token>
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('ApiToken '):
            return jsonify({'errors': [{'code': 4010010, 'detail': 'Authentication required', 'title': 'Unauthorized'}]}), 401
        token = auth_header[len('ApiToken '):]
        if token != Config.API_TOKEN:
            return jsonify({'errors': [{'code': 4010010, 'detail': 'Invalid token', 'title': 'Unauthorized'}]}), 401
        return f(*args, **kwargs)
    return decorated

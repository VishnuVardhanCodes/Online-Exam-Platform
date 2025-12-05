from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from database import User

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception:
            return jsonify({'error': 'Invalid or expired token'}), 401
    return decorated

def role_required(*allowed_roles):
    """Decorator to require specific user roles"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                user = User.query.get(user_id)
                
                if not user or user.role not in allowed_roles:
                    return jsonify({'error': 'Insufficient permissions'}), 403
                
                return f(*args, **kwargs)
            except Exception:
                return jsonify({'error': 'Authentication failed'}), 401
        return decorated
    return decorator

def validate_request_json(required_fields):
    """Decorator to validate JSON request has required fields"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            from flask import request
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'Request body is required'}), 400
            
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
            
            return f(*args, **kwargs)
        return decorated
    return decorator

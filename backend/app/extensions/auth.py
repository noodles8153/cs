import jwt
from flask import request, g, current_app, abort
from functools import wraps

def jwt_required(roles=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization', '').split('Bearer ')[-1]
            if not token:
                abort(401, description="缺少认证令牌")
            
            try:
                payload = jwt.decode(
                    token,
                    current_app.config['SECRET_KEY'],
                    algorithms=['HS256']
                )
                
                if roles and payload.get('role') not in roles:
                    abort(403, description="权限不足")
                
                g.current_user = payload
            except jwt.ExpiredSignatureError:
                abort(401, description="令牌已过期")
            except jwt.InvalidTokenError:
                abort(401, description="无效令牌")
                
            return fn(*args, **kwargs)
        return wrapper
    return decorator
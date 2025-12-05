from flask import session, redirect, url_for
from functools import wraps

def login_required(roles=None):
    """
    roles: None (any logged user) or string or list/tuple of roles.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("auth.login"))

            if roles:
                if isinstance(roles, str):
                    allowed = [roles]
                else:
                    allowed = list(roles)

                if session.get("role") not in allowed:
                    return "Unauthorized", 403
            return fn(*args, **kwargs)
        return decorated
    return wrapper

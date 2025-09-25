from django.core.exceptions import PermissionDenied
from functools import wraps


def role_required(allowed_roles):
    """
    Decorator to restrict view access to one or more roles.

    Usage:
        @role_required('ADMIN')
        @role_required(['ADMIN', 'RECRUITER'])
    """
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied("User must be logged in")
            if not hasattr(request.user, 'userprofile'):
                raise PermissionDenied("User profile not found")
            if request.user.userprofile.role not in allowed_roles:
                raise PermissionDenied(f"Access denied: {', '.join(allowed_roles)} role required")
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator

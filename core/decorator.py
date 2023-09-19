from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect


def staff_member_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Access Denied')
            return redirect('main:admin_login')
    return wrapper

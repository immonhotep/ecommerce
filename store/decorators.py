from django.shortcuts import redirect
from django.contrib import messages

def user_is_superuser(function=None, redirect_url='/'):

    """
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_superuser:
                messages.error(request,'You have no permission')
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    if function:
        return decorator(function)
    return decorator


def user_not_authenticated(function=None, redirect_url='/'):
    """
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            
            return view_func(request, *args, **kwargs)    
        return _wrapped_view 
    if function:
        return decorator(function)
    return decorator

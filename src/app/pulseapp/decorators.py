from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('pulseapp:index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = list(request.user.groups.all().values_list("name",flat=True))
                if any(x in group for x in allowed_roles):
                    return view_func(request, *args, **kwargs)
                else:
                    if group[0]=='admin':
                        return redirect('pulseapp:viewsampledata')
                    elif group[0]=='trends':
                        return redirect('pulseapp:viewtrends')
                    elif group[0]=='variants':
                        return redirect('pulseapp:viewvariants')
                    else:
                        return redirect('pulseapp:index')
            else:
                return redirect('pulseapp:index')

        return wrapper_func
    return decorator

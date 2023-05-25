from django.shortcuts import redirect, render
from django.contrib.auth.models import Group


def check_auth_redirect(login_page):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return login_page(request, *args, **kwargs)

    return wrapper_func



def allowed_users(allowed_group):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            try:
                group = request.user.groups.get(name=allowed_group)
                return view_func(request)
            except Group.DoesNotExist:
                pass

            if not group:
                try:
                    group = request.user.groups.get(name='Technicians')
                    return redirect("home_techs")
                except Group.DoesNotExist:
                    return redirect("home_non_it")

            

        return wrapper_func

    return decorator

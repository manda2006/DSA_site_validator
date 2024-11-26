from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home(request):
    return redirect('challenge_list')

def redirect_authenticated_user(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('challenge_list')
        return view(request, *args, **kwargs)
    return wrapper

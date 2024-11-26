from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home(request):
    return render(request, 'accounts/home.html')

def redirect_authenticated_user(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view(request, *args, **kwargs)
    return wrapper

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Page de connexion
    path('', views.redirect_authenticated_user(auth_views.LoginView.as_view(template_name='accounts/login.html')), name='login'),
    # Page d'accueil pour les utilisateurs connectés
    path('home/', views.home, name='home'),
    # Page de déconnexion
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

from django.urls import path
from .views import challenge_detail, challenge_list, fetch_defined_files

urlpatterns = [
    path('challenges/', challenge_list, name='challenge_list'),
    path('<str:challenge_slug>/', challenge_detail, name='challenge_detail'),
    path('<str:challenge_slug>/fetch-defined-files/', fetch_defined_files, name='fetch_defined_files'),
]
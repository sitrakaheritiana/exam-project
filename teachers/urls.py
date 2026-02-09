from django.urls import path
from .views import teacher_profile

app_name = 'teachers'

urlpatterns = [
    path('profile/', teacher_profile, name='profile'),
]

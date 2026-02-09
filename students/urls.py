from django.urls import path
from .views import student_profile

app_name = 'students'

urlpatterns = [
    path('profile/', student_profile, name='profile'),
]

from django.urls import path
from . import views

app_name = 'formations'

urlpatterns = [
    path('', views.formation_list, name='list'),
    path('create/', views.formation_create, name='create'),
    path('update/<int:pk>/', views.formation_update, name='update'),
    path('delete/<int:pk>/', views.formation_delete, name='delete'),
]

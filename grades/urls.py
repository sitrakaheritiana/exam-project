from django.urls import path
from . import views

app_name = 'grades'

urlpatterns = [
    path('', views.grade_list, name='list'),
    path('create/', views.grade_create, name='create'),
    path('student/', views.student_grades, name='student_grades'),
    path('student/pdf/', views.download_transcript_view, name='download_pdf'),
]

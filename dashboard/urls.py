from django.urls import path
from . import views

app_name = 'dashboard'   # 🔥 OBLIGATOIRE

urlpatterns = [
    path('', views.dashboard_router, name='dashboard'),
    path('student/', views.student_dashboard, name='student'),
    path('teacher/', views.teacher_dashboard, name='teacher'),
    path('admin/', views.admin_dashboard, name='admin'),
    path('admin/students/', views.student_list, name='students'),
    path('admin/teachers/', views.teacher_list, name='teachers'),
    path('admin/students/create/', views.student_create, name='student_create'),
    path('admin/teachers/create/', views.teacher_create, name='teacher_create'),
    path('admin/students/<int:pk>/', views.student_detail, name='student_detail'),
    path('admin/students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('admin/teachers/<int:pk>/edit/', views.teacher_update, name='teacher_update'),

]

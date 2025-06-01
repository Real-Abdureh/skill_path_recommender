from django.urls import path
from . import views


"""
URL Configuration for the learning_paths app.
"""
from django.urls import path
from . import views

app_name = 'learning_paths'

urlpatterns = [
    path('', views.learning_path_list, name='learning_path_list'),
    path('<int:path_id>/', views.learning_path_detail, name='learning_path_detail'),
    path('generate/', views.generate_path, name='generate_path'),
    path('public/', views.public_paths, name='public_paths'),
    path('step/<int:step_id>/complete/', views.mark_step_completed, name='mark_step_completed'),
    path('step/<int:step_id>/incomplete/', views.mark_step_incomplete, name='mark_step_incomplete'),
    path('career/<int:career_id>/', views.learning_path_for_career_view, name='learning_path_for_career'),
]



from django.urls import path
from . import views

app_name = 'learning_paths'

urlpatterns = [
    path('career/<int:career_id>/', views.learning_path_detail, name='learning_path_for_career'),
]

from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    path('', views.career_list, name='career_list'),
    path('<int:career_id>/', views.career_detail, name='career_detail'),
]

from django.urls import path
from . import views


app_name = 'careers'

urlpatterns = [
    path('', views.careers_list, name='careers_list'),
    path('<int:career_id>/', views.career_detail, name='career_detail'),
    path('selection/', views.career_selection, name='career_selection'),
    path('skills/', views.skills_list, name='skills_list'),
    path('skills/<int:skill_id>/', views.skill_detail, name='skill_detail'),
    path('resources/', views.resources_list, name='resources_list'),
    path('resources/<int:resource_id>/', views.resource_detail, name='resource_detail'),
]



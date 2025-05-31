"""
URL Configuration for the accounts app.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=CustomAuthenticationForm,
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('skills/add/', views.add_user_skill, name='add_user_skill'),
    path('skills/remove/<int:skill_id>/', views.remove_user_skill, name='remove_user_skill'),
    path('select_career_goal/<int:career_id>/', views.select_career_goal, name='select_career_goal'),
    path('clear_career_goal/', views.clear_career_goal, name='clear_career_goal'),
]
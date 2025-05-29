from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm # Used by LoginView if not overridden by a custom form
from django.contrib.auth.views import LoginView # Will be used in urls.py
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from .forms import SignUpForm, UserUpdateForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, UserProfileForm, UserUpdateForm
from .models import UserProfile, UserSkill
from careers.models import Skill
from learning_paths.models import LearningPath, PathStep, UserPathProgress
from django.contrib.auth.models import User

def home(request):
    """
    Home page view showing site introduction and features
    """
    return render(request, 'home.html')

@login_required
def dashboard(request):
    """
    User dashboard showing learning progress, recent activity, and recommendations
    """
    # Get active learning paths
    active_paths = []
    paths = LearningPath.objects.filter(users=request.user)
    
    for path in paths:
        # Get path progress information
        total_steps = PathStep.objects.filter(learning_path=path).count()
        completed_steps = UserPathProgress.objects.filter(
            user=request.user,
            path_step__learning_path=path, 
            completed=True
        ).count()
        
        if total_steps > 0:
            progress = int((completed_steps / total_steps) * 100)
        else:
            progress = 0
            
        if progress < 100:  # Only add to active paths if not completed
            active_paths.append({
                'id': path.id,
                'title': path.title,
                'steps_completed': completed_steps,
                'total_steps': total_steps,
                'progress': progress
            })
    
    # Get total completed steps
    completed_steps = UserPathProgress.objects.filter(
        user=request.user,
        completed=True
    ).count()
    
    # Get recent activities
    # This would typically be from an Activity model
    # For now we'll create mock data
    recent_activities = [
        # Sample activities - in a real implementation, these would come from the database
        {
            'type': 'path_started',
            'description': 'Started learning path: Full Stack Web Development',
            'timestamp': '2023-10-15T14:30:00Z'
        },
        {
            'type': 'step_completed',
            'description': 'Completed: Introduction to HTML/CSS',
            'timestamp': '2023-10-16T09:45:00Z'
        }
    ] if active_paths else []
    
    # Get recommended resources
    # In a real implementation, these would be based on the user's learning paths and skills
    recommended_resources = []
    
    context = {
        'active_paths': active_paths,
        'completed_steps': completed_steps,
        'recent_activities': recent_activities,
        'recommended_resources': recommended_resources,
    }
    
    return render(request, 'accounts/dashboard.html', context)

def signup(request):
    """
    User registration view
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create a UserProfile for the new user
            UserProfile.objects.create(user=user)
            
            # Log the user in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, 'Your account has been created successfully!')
            return redirect('profile_update')  # Redirect to profile update to complete profile
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile_update(request):
    """
    View for updating user profile information
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        
        # Make sure user profile exists
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('dashboard')
    else:
        user_form = UserUpdateForm(instance=request.user)
        
        # Make sure user profile exists
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    # Get user's existing skills
    user_skills = UserSkill.objects.filter(user=request.user)
    
    # Get available skills that the user doesn't have yet
    existing_skill_ids = user_skills.values_list('skill_id', flat=True)
    available_skills = Skill.objects.exclude(id__in=existing_skill_ids)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_skills': user_skills,
        'available_skills': available_skills
    }
    
    return render(request, 'accounts/profile_update.html', context)

@login_required
def add_user_skill(request):
    """
    Add a skill to the user's profile
    """
    if request.method == 'POST':
        skill_id = request.POST.get('skill_id')
        proficiency = request.POST.get('proficiency')
        
        # Validate input
        if not skill_id or not proficiency:
            messages.error(request, 'Invalid form data')
            return redirect('profile_update')
        
        # Check if skill exists
        try:
            skill = Skill.objects.get(id=skill_id)
        except Skill.DoesNotExist:
            messages.error(request, 'Skill not found')
            return redirect('profile_update')
        
        # Check if user already has this skill
        if UserSkill.objects.filter(user=request.user, skill=skill).exists():
            messages.warning(request, f'You already have "{skill.name}" in your skills')
        else:
            # Add skill to user's profile
            UserSkill.objects.create(
                user=request.user,
                skill=skill,
                proficiency=proficiency
            )
            messages.success(request, f'"{skill.name}" added to your skills')
    
    return redirect('profile_update')

@login_required
def remove_user_skill(request, skill_id):
    """
    Remove a skill from the user's profile
    """
    user_skill = get_object_or_404(UserSkill, id=skill_id, user=request.user)
    skill_name = user_skill.skill.name
    user_skill.delete()
    messages.success(request, f'"{skill_name}" removed from your skills')
    return redirect('profile_update')















def home(request): # Keep the existing home view
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:dashboard') # Or 'home' or wherever you want to redirect after signup
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

# Using a function-based view for profile update for consistency with signup
@login_required
def profile_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Your profile was successfully updated!') # Optional: Add messages
            return redirect('accounts:dashboard') # Or to a profile page
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/profile_update.html', {'form': form})

# LoginView and LogoutView will be configured in urls.py
# No custom view code needed here for them if using Django's defaults with template_name.

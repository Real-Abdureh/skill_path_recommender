from django.shortcuts import render, get_object_or_404
from .models import LearningPath, PathStep, LearningResource
from careers.models import Career
from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import LearningPath, PathStep, UserPathProgress
from .recommendation import generate_learning_path
from careers.models import Career, Skill
from accounts.models import UserSkill

@login_required
def learning_path_list(request):
    """
    View to display a list of the user's learning paths
    """
    # Get all paths the user is enrolled in
    user_paths = LearningPath.objects.filter(users=request.user)
    
    # Process path progress information
    paths_with_progress = []
    for path in user_paths:
        total_steps = PathStep.objects.filter(learning_path=path).count()
        completed_steps = UserPathProgress.objects.filter(
            user=request.user,
            path_step__learning_path=path,
            completed=True
        ).count()
        
        # Calculate progress percentage
        if total_steps > 0:
            progress = int((completed_steps / total_steps) * 100)
        else:
            progress = 0
        
        # Add path with progress info to the list
        paths_with_progress.append({
            'path': path,
            'total_steps': total_steps,
            'completed_steps': completed_steps,
            'progress': progress,
            'is_completed': progress == 100
        })
    
    # Separate completed and active paths
    active_paths = [p for p in paths_with_progress if not p['is_completed']]
    completed_paths = [p for p in paths_with_progress if p['is_completed']]
    
    context = {
        'active_paths': active_paths,
        'completed_paths': completed_paths
    }
    
    return render(request, 'learning_paths/path_list.html', context)

@login_required
def learning_path_detail(request, path_id):
    """
    View to display detailed information about a learning path and its steps
    """
    # Get the learning path
    path = get_object_or_404(LearningPath, id=path_id)
    
    # Check if the user has access to this path
    if request.user not in path.users.all() and not path.is_public:
        messages.error(request, "You don't have access to this learning path.")
        return redirect('learning_path_list')
    
    # Get all steps in the path
    steps = PathStep.objects.filter(learning_path=path).order_by('order')
    
    # Get user's progress for each step
    steps_with_progress = []
    for step in steps:
        progress, created = UserPathProgress.objects.get_or_create(
            user=request.user,
            path_step=step,
            defaults={'completed': False}
        )
        
        steps_with_progress.append({
            'step': step,
            'completed': progress.completed,
            'completion_date': progress.completion_date
        })
    
    # Calculate overall path progress
    total_steps = len(steps)
    completed_steps = sum(1 for swp in steps_with_progress if swp['completed'])
    
    if total_steps > 0:
        progress_percentage = int((completed_steps / total_steps) * 100)
    else:
        progress_percentage = 0
    
    context = {
        'path': path,
        'steps': steps_with_progress,
        'progress_percentage': progress_percentage,
        'completed_steps': completed_steps,
        'total_steps': total_steps
    }
    
    return render(request, 'learning_paths/path_detail.html', context)

@login_required
def generate_path(request):
    """
    View to generate a personalized learning path based on user's career selection
    """
    if request.method == 'POST':
        career_id = request.POST.get('career_id')
        
        if not career_id:
            messages.error(request, 'Please select a career to generate a learning path.')
            return redirect('career_selection')
            
        try:
            career = Career.objects.get(id=career_id)
            
            # Get user's existing skills
            user_skills = UserSkill.objects.filter(user=request.user)
            existing_skill_ids = [us.skill.id for us in user_skills]
            
            # Generate the learning path using the recommendation engine
            learning_path = generate_learning_path(
                user=request.user,
                career=career,
                existing_skill_ids=existing_skill_ids
            )
            
            messages.success(request, f'Your personalized learning path for {career.name} has been created.')
            return redirect('learning_path_detail', path_id=learning_path.id)
            
        except Career.DoesNotExist:
            messages.error(request, 'Invalid career selection.')
            return redirect('careers:career_selection')
        except Exception as e:
            messages.error(request, f'Error generating learning path: {str(e)}')
            return redirect('careers:career_selection')

    
    # GET requests should go to career selection
    return redirect('careers:career_selection')

def learning_path_for_career_view(request, career_id):
    career = get_object_or_404(Career, pk=career_id)
    # This picks the first learning path if a career has multiple.
    learning_path = LearningPath.objects.filter(career=career).first() 
    
    steps = []
    if learning_path:
        steps = learning_path.steps.all().prefetch_related(
            Prefetch('resources', queryset=LearningResource.objects.all()) # 'resources' (plural)
        )
    
    context = {
        'career': career,
        'learning_path': learning_path,
        'steps': steps
    }
    # This reuses your existing template for displaying a path.
    # Ensure 'learning_paths/path_detail.html' can handle 'learning_path' being None.
    return render(request, 'learning_paths/path_detail.html', context)

@login_required
def mark_step_completed(request, step_id):
    """
    View to mark a step in a learning path as completed
    """
    if request.method == 'POST':
        step = get_object_or_404(PathStep, id=step_id)
        
        # Check if user has access to the path
        if request.user not in step.learning_path.users.all():
            messages.error(request, "You don't have access to this learning path.")
            return redirect('learning_path_list')
        
        # Update progress
        progress, created = UserPathProgress.objects.get_or_create(
            user=request.user,
            path_step=step,
            defaults={'completed': True, 'completion_date': timezone.now()}
        )
        
        if not created:
            progress.completed = True
            progress.completion_date = timezone.now()
            progress.save()
        
        messages.success(request, f'Marked "{step.title}" as completed!')
        
        # Redirect back to path detail
        return redirect('learning_path_detail', path_id=step.learning_path.id)
    
    # If not POST, redirect to learning paths list
    return redirect('learning_path_list')

@login_required
def mark_step_incomplete(request, step_id):
    """
    View to mark a step in a learning path as not completed
    """
    if request.method == 'POST':
        step = get_object_or_404(PathStep, id=step_id)
        
        # Check if user has access to the path
        if request.user not in step.learning_path.users.all():
            messages.error(request, "You don't have access to this learning path.")
            return redirect('learning_path_list')
        
        # Update progress
        progress, created = UserPathProgress.objects.get_or_create(
            user=request.user,
            path_step=step,
            defaults={'completed': False, 'completion_date': None}
        )
        
        if not created:
            progress.completed = False
            progress.completion_date = None
            progress.save()
        
        messages.success(request, f'Marked "{step.title}" as not completed.')
        
        # Redirect back to path detail
        return redirect('learning_path_detail', path_id=step.learning_path.id)
    
    # If not POST, redirect to learning paths list
    return redirect('learning_path_list')

def public_paths(request):
    """
    View to display a list of public learning paths
    """
    # Get search parameter
    search_query = request.GET.get('search', '')
    career_filter = request.GET.get('career', '')
    
    # Filter public paths
    paths = LearningPath.objects.filter(is_public=True)
    
    if search_query:
        paths = paths.filter(title__icontains=search_query)
        
    if career_filter:
        paths = paths.filter(career__id=career_filter)
    
    # Get careers for filtering
    careers = Career.objects.all()
    
    context = {
        'paths': paths,
        'search_query': search_query,
        'career_filter': career_filter,
        'careers': careers,
    }
    
    return render(request, 'learning_paths/public_paths.html', context)


from django.shortcuts import render, get_object_or_404
from .models import Career

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Career, Skill, LearningResource

def careers_list(request):
    """
    View to display a list of all available careers
    """
    # Get search parameter
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    # Filter careers by search query and category
    careers = Career.objects.all()
    
    if search_query:
        careers = careers.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
        
    if category_filter:
        careers = careers.filter(category=category_filter)
    
    # Get all unique categories for the filter dropdown
    categories = Career.objects.values_list('category', flat=True).distinct()
    categories = [c for c in categories if c]  # Remove empty categories
    
    context = {
        'careers': careers,
        'search_query': search_query,
        'category_filter': category_filter,
        'categories': categories,
    }
    
    return render(request, 'careers/career_list.html', context)

def career_detail(request, career_id):
    """
    View to display details of a specific career
    """
    career = get_object_or_404(Career, id=career_id)
    
    # Get the essential skills for this career
    essential_skills = career.required_skills.filter(careerskill__importance='essential')
    important_skills = career.required_skills.filter(careerskill__importance='important')
    useful_skills = career.required_skills.filter(careerskill__importance='useful')
    
    # Get learning paths related to this career
    learning_paths = career.learning_paths.filter(is_public=True)[:5]
    
    context = {
        'career': career,
        'essential_skills': essential_skills,
        'important_skills': important_skills,
        'useful_skills': useful_skills,
        'learning_paths': learning_paths,
    }
    
    return render(request, 'careers/career_detail.html', context)

@login_required
def career_selection(request):
    """
    View for users to select a career for path recommendation
    """
    # Get search parameter
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    # Filter careers by search query and category
    careers = Career.objects.all()
    
    if search_query:
        careers = careers.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
        
    if category_filter:
        careers = careers.filter(category=category_filter)
    
    # Get all unique categories for the filter dropdown
    categories = Career.objects.values_list('category', flat=True).distinct()
    categories = [c for c in categories if c]  # Remove empty categories
    
    context = {
        'careers': careers,
        'search_query': search_query,
        'category_filter': category_filter,
        'categories': categories,
    }
    
    return render(request, 'careers/career_selection.html', context)

def skills_list(request):
    """
    View to display a list of all available skills
    """
    # Get search parameter
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    # Filter skills by search query and category
    skills = Skill.objects.all()
    
    if search_query:
        skills = skills.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
        
    if category_filter:
        skills = skills.filter(category=category_filter)
    
    # Get all unique categories for the filter dropdown
    categories = Skill.objects.values_list('category', flat=True).distinct()
    
    context = {
        'skills': skills,
        'search_query': search_query,
        'category_filter': category_filter,
        'categories': categories,
    }
    
    return render(request, 'careers/skill_list.html', context)

def skill_detail(request, skill_id):
    """
    View to display details of a specific skill
    """
    skill = get_object_or_404(Skill, id=skill_id)
    
    # Get careers that require this skill
    careers = skill.careers.all()
    
    # Get learning resources for this skill
    resources = skill.resources.all()
    
    context = {
        'skill': skill,
        'careers': careers,
        'resources': resources,
    }
    
    return render(request, 'careers/skill_detail.html', context)

def resources_list(request):
    """
    View to display a list of all available learning resources
    """
    # Get filter parameters
    search_query = request.GET.get('search', '')
    type_filter = request.GET.get('type', '')
    difficulty_filter = request.GET.get('difficulty', '')
    free_filter = request.GET.get('free', '')
    
    # Filter resources
    resources = LearningResource.objects.all()
    
    if search_query:
        resources = resources.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
        
    if type_filter:
        resources = resources.filter(resource_type=type_filter)
        
    if difficulty_filter:
        resources = resources.filter(difficulty=difficulty_filter)
        
    if free_filter:
        is_free = free_filter == 'true'
        resources = resources.filter(is_free=is_free)
    
    # Get filter options
    resource_types = dict(LearningResource.RESOURCE_TYPES)
    difficulty_levels = dict(LearningResource.DIFFICULTY_LEVELS)
    
    context = {
        'resources': resources,
        'search_query': search_query,
        'type_filter': type_filter,
        'difficulty_filter': difficulty_filter,
        'free_filter': free_filter,
        'resource_types': resource_types,
        'difficulty_levels': difficulty_levels,
    }
    
    return render(request, 'careers/resource_list.html', context)

def resource_detail(request, resource_id):
    """
    View to display details of a specific learning resource
    """
    resource = get_object_or_404(LearningResource, id=resource_id)
    
    # Get related skills
    skills = resource.skills.all()
    
    context = {
        'resource': resource,
        'skills': skills,
    }
    
    return render(request, 'careers/resource_detail.html', context)



def career_list(request):
    careers = Career.objects.all()
    return render(request, 'careers/career_list.html', {'careers': careers})

def career_detail(request, career_id):
    career = get_object_or_404(Career, pk=career_id)
    # Required skills can be accessed in the template via career.required_skills.all
    return render(request, 'careers/career_detail.html', {'career': career})

from django.shortcuts import render, get_object_or_404
from .models import LearningPath, LearningPathStep, LearningResource
from careers.models import Career

def learning_path_detail(request, career_id):
    career = get_object_or_404(Career, pk=career_id)
    learning_path = LearningPath.objects.filter(career=career).first()
    steps = []
    if learning_path:
        steps = learning_path.steps.all().prefetch_related('resources')
    
    context = {
        'career': career,
        'learning_path': learning_path,
        'steps': steps
    }
    return render(request, 'learning_paths/path_detail.html', context)

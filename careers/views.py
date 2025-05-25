from django.shortcuts import render, get_object_or_404
from .models import Career

def career_list(request):
    careers = Career.objects.all()
    return render(request, 'careers/career_list.html', {'careers': careers})

def career_detail(request, career_id):
    career = get_object_or_404(Career, pk=career_id)
    # Required skills can be accessed in the template via career.required_skills.all
    return render(request, 'careers/career_detail.html', {'career': career})

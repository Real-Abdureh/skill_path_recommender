from django.contrib import admin
from .models import LearningResource, LearningPath, PathStep

admin.site.register(LearningResource)
admin.site.register(LearningPath)
admin.site.register(PathStep)

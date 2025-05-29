from django.db import models
from django.contrib.auth.models import User
from careers.models import Career, Skill, LearningResource

class LearningPath(models.Model):
    """Model for customized learning paths"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_paths')
    users = models.ManyToManyField(User, related_name='enrolled_paths')
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='learning_paths')
    skills = models.ManyToManyField(Skill, related_name='learning_paths')
    duration_weeks = models.PositiveIntegerField(default=0)  # Estimated completion time
    is_public = models.BooleanField(default=False)  # Whether path is visible to other users
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class PathStep(models.Model):
    """Model for individual steps in a learning path"""
    STEP_TYPES = (
        ('skill', 'Learn Skill'),
        ('resource', 'Complete Resource'),
        ('project', 'Complete Project'),
        ('assessment', 'Pass Assessment'),
    )
    
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=200)
    description = models.TextField()
    step_type = models.CharField(max_length=20, choices=STEP_TYPES, default='skill')
    order = models.PositiveIntegerField()  # To determine step order in the path
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True, blank=True)
    resource = models.ForeignKey(LearningResource, on_delete=models.CASCADE, null=True, blank=True)
    estimated_hours = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f'{self.learning_path.title} - Step {self.order}: {self.title}'

class UserPathProgress(models.Model):
    """Model to track user progress through learning paths"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    path_step = models.ForeignKey(PathStep, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'path_step']
    
    def __str__(self):
        status = 'Completed' if self.completed else 'In Progress'
        return f'{self.user.username} - {self.path_step.title} ({status})'




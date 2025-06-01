from django.db import models
from django.contrib.auth.models import User
from careers.models import Career, Skill, LearningResource # LearningResource imported here

class LearningPath(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_paths')
    users = models.ManyToManyField(User, related_name='enrolled_paths', blank=True)
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='learning_paths_for_career')
    skills = models.ManyToManyField(Skill, related_name='learning_paths_targeting_skill', blank=True)
    duration_weeks = models.PositiveIntegerField(default=0, help_text="Estimated completion time in weeks")
    is_public = models.BooleanField(default=False, help_text="Whether path is visible to other users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PathStep(models.Model):
    STEP_TYPES = (
        ('skill', 'Learn Skill'),
        ('resource', 'Complete Resource'),
        ('project', 'Complete Project'),
        ('assessment', 'Pass Assessment'),
    )
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=200)
    description = models.TextField()
    step_type = models.CharField(max_length=20, choices=STEP_TYPES, default='resource')
    order = models.PositiveIntegerField(help_text="Order of the step in the path")
    skill_to_learn = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name="path_steps_for_skill")
    resources = models.ManyToManyField(LearningResource, blank=True, related_name='path_steps_featuring_resource') # Now ManyToMany
    estimated_hours = models.PositiveIntegerField(default=0, help_text="Estimated hours to complete this step")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        unique_together = ('learning_path', 'order')

    def __str__(self):
        return f'{self.learning_path.title} - Step {self.order}: {self.title}'

class UserPathProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='path_progress')
    path_step = models.ForeignKey(PathStep, on_delete=models.CASCADE, related_name='user_progress_entries')
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'path_step')

    def __str__(self):
        status = 'Completed' if self.completed else 'In Progress'
        return f'{self.user.username} - {self.path_step.title} ({status})'
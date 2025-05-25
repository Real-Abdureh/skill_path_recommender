from django.db import models
from careers.models import Skill, Career # Ensure careers.models is created first

class LearningResource(models.Model):
    RESOURCE_TYPES = [
        ('course', 'Course'),
        ('tool', 'Tool'),
        ('article', 'Article'),
        ('book', 'Book'),
        ('video', 'Video'),
    ]
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=500)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    skills = models.ManyToManyField(Skill, blank=True, related_name='resources_for_skill')
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title

class LearningPath(models.Model):
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='learning_paths')
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_paths') # If paths are user-specific
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # skills_to_develop = models.ManyToManyField(Skill, related_name='learning_paths_developing_skill') # Optional: if path focuses on specific skills beyond career

    def __str__(self):
        return f'{self.career.name} - {self.title}'

class LearningPathStep(models.Model):
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField()
    resources = models.ManyToManyField(LearningResource, blank=True, related_name='steps_using_resource')
    # skills_covered = models.ManyToManyField(Skill, blank=True, related_name='steps_covering_skill') # Optional

    def __str__(self):
        return f'{self.learning_path.title} - Step {self.order}: {self.title}'

    class Meta:
        ordering = ['order']

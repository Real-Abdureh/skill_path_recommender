from django.db import models

from django.utils.text import slugify

class Career(models.Model):
    """Model for career paths"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=50, blank=True)
    average_salary = models.CharField(max_length=50, blank=True)
    job_outlook = models.TextField(blank=True)
    required_education = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
class Skill(models.Model):
    """Model for skills that can be learned"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=50)  # e.g., Technical, Soft Skill, Tool
    careers = models.ManyToManyField(Career, related_name='required_skills', through='CareerSkill')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class CareerSkill(models.Model):
    """Model for the relationship between careers and skills with importance level"""
    IMPORTANCE_LEVELS = (
        ('essential', 'Essential'),
        ('important', 'Important'),
        ('useful', 'Useful'),
    )
    
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    importance = models.CharField(max_length=20, choices=IMPORTANCE_LEVELS, default='important')
    
    class Meta:
        unique_together = ['career', 'skill']
    
    def __str__(self):
        return f'{self.career.name} - {self.skill.name} ({self.importance})'

class LearningResource(models.Model):
    """Model for learning resources linked to skills"""
    RESOURCE_TYPES = (
        ('course', 'Online Course'),
        ('book', 'Book'),
        ('video', 'Video Tutorial'),
        ('article', 'Article'),
        ('documentation', 'Documentation'),
        ('tool', 'Interactive Tool'),
        ('other', 'Other'),
    )
    
    DIFFICULTY_LEVELS = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('all', 'All Levels'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField(max_length=500)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='all')
    skills = models.ManyToManyField(Skill, related_name='resources')
    duration = models.CharField(max_length=50, blank=True)  # e.g., "2 hours", "4 weeks"
    is_free = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)  # 1.0 to 5.0
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title








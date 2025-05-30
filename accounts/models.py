from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from careers.models import Skill, Career

class UserProfile(models.Model):
    """Extended user profile model"""
    EXPERIENCE_LEVELS = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    selected_career = models.ForeignKey(
    Career,
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name='users_with_this_goal'
)
    current_position = models.CharField(max_length=100, blank=True)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS, default='beginner')
    learning_goal = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"


class UserSkill(models.Model):
    """Model to track user skills and proficiency levels"""
    PROFICIENCY_LEVELS = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey('careers.Skill', on_delete=models.CASCADE)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS, default='beginner')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'skill']
        
    def __str__(self):
        return f'{self.user.username} - {self.skill.name} ({self.get_proficiency_display()})'


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    # For existing users, just save the profile.
    # It's important that the related_name 'profile' is used here.
    # This assumes that if a User instance is saved, its profile should also be saved.
    # This might be redundant if profile updates are handled separately,
    # but ensures the profile is saved if the User instance is saved for other reasons.
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # This case might occur if a User was somehow created without triggering the initial profile creation.
        # Or if the profile was deleted manually.
        UserProfile.objects.create(user=instance)

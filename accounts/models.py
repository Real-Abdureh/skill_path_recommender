from django.db import models
from django.contrib.auth.models import User
from careers.models import Skill # Ensure careers.models is created first or this will fail
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    current_skills = models.ManyToManyField(Skill, blank=True, related_name='user_profiles_with_skill')
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

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

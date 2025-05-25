from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Career(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    required_skills = models.ManyToManyField(Skill, related_name='careers_requiring_skill')

    def __str__(self):
        return self.name

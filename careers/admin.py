from django.contrib import admin
from .models import Skill, Career

# Unregister the models if they were previously registered simply
# (This might not be strictly necessary if the overwrite_file_with_block replaces all content,
# but it's good practice if we were appending or selectively modifying)
# However, since we are overwriting, these unregister calls are not strictly needed here.
# try:
#     admin.site.unregister(Skill)
# except admin.sites.NotRegistered:
#     pass
# try:
#     admin.site.unregister(Career)
# except admin.sites.NotRegistered:
#     pass

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class CareerAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    filter_horizontal = ('required_skills',) # Use filter_horizontal for ManyToManyField

admin.site.register(Skill, SkillAdmin)
admin.site.register(Career, CareerAdmin)

from django.contrib import admin
from .models import Skill, Career, CareerSkill

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
class CareerSkillInline(admin.TabularInline):
    model = CareerSkill
    extra = 1

class CareerAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    inlines = [CareerSkillInline]

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(Skill, SkillAdmin)
admin.site.register(Career, CareerAdmin)
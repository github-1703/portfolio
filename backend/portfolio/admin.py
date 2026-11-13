from django.contrib import admin
from .models import Profile,Project,Skill,Education,Experience,ContactMessage


class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ("technologies",)

# Register your models here.
admin.site.register(Profile)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Skill)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(ContactMessage)


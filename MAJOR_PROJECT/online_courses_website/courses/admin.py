from django.contrib import admin
from .models import Contact, Course, CourseModule, Profile , Faculty

admin.site.register(Contact)
admin.site.register(Course)
admin.site.register(CourseModule)
admin.site.register(Profile)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation')

admin.site.register(Faculty, FacultyAdmin)

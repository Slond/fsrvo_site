from django.contrib import admin
from django.contrib.auth.models import User
from .models import *

class NewsAdmin(admin.ModelAdmin):
    list_filter = ('date', 'author')
    list_display = ['author', '__str__', 'date']

class StudentAdmin(admin.ModelAdmin):
    list_filter = ('teacher', 'school_name', 'number')
    list_display = ['__str__','school_name', 'login', 'rank', 'number', 'teacher']
    def login(self, obj):
        return obj.user.username


admin.site.register(Student, StudentAdmin)
admin.site.register(School)
admin.site.register(News, NewsAdmin)

admin.site.register(Quiz)

class AskAdmin(admin.ModelAdmin):
    list_filter = ('article','date')

admin.site.register(Asks, AskAdmin)
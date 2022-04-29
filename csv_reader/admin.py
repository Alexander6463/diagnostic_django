from django.contrib import admin

from .models import Question, User, Answers

# Register your models here.

admin.site.register(Question)
admin.site.register(User)
admin.site.register(Answers)

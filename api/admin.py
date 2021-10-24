from django.contrib import admin

# Register your models here.
from .models import Film, Comment

admin.site.register(Film)
admin.site.register(Comment)
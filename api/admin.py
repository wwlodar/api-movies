from django.contrib import admin

# Register your models here.
from .models import Movie, Comment, Ratings

admin.site.register(Movie)
admin.site.register(Comment)
admin.site.register(Ratings)
from django.db.models import Q
from .models import Movie
import django_filters


class MoviesFilter(django_filters.FilterSet):
  language = django_filters.CharFilter(method="language_filter")
  genre = django_filters.CharFilter(method="genre_filter")
  country = django_filters.CharFilter(method="country_filter")
  
  class Meta:
    model = Movie
    fields = ['language', 'genre', 'country']
  
  def language_filter(self, queryset, name, value):
    query = Movie.objects.all()
    for language in value.split(","):
      query = query.filter(Language__contains=language)
    return query
  
  def genre_filter(self, queryset, name, value):
    query = Movie.objects.all()
    for genre in value.split(","):
      query = query.filter(Genre__contains=genre)
    return query
  
  def country_filter(self, queryset, name, value):
    query = Movie.objects.all()
    for country in value.split(","):
      query = query.filter(Country__contains=country)
    return query

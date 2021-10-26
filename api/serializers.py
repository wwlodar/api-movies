from rest_framework import serializers
from .models import Movie, Ratings, Comment


class RatingsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Ratings
    fields = ('Source', 'Value')


class MovieSerializer(serializers.ModelSerializer):
  Ratings = RatingsSerializer(many=True)
  
  class Meta:
    model = Movie
    fields = ('id', 'Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre', 'Director', 'Writer', 'Actors', 'Plot',
              'Language', 'Country', 'Awards', 'Poster', 'Metascore', 'imdbRating', 'imdbVotes',
              'imdbID', 'Type', 'DVD', 'BoxOffice', 'Production', 'Website', 'Ratings')
    extra_kwargs = {
      'Title': {'validators': []},
    }
  
  def __init__(self, *args, **kwargs):
    # Don't pass the 'fields' arg up to the superclass
    fields = kwargs.pop('fields', None)
    
    # Instantiate the superclass normally
    super(MovieSerializer, self).__init__(*args, **kwargs)
    
    if fields:
      # Drop any fields that are not specified in the `fields` argument.
      allowed = set(fields)
      existing = set(self.fields.keys())
      for field_name in existing - allowed:
        self.fields.pop(field_name)
  
  def create(self, validated_data):
    ratings_validated_data = validated_data.pop('Ratings')
    data_imdbVotes = validated_data.pop('imdbVotes')
    validated_data['imdbVotes'] = data_imdbVotes.replace(',', '')
    movie, created = Movie.objects.get_or_create(**validated_data)
    for rating in ratings_validated_data:
      Ratings.objects.get_or_create(movie=movie, **rating)
    return movie


class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'

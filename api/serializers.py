from rest_framework import serializers
from .models import Film, Ratings, Comment


class RatingsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Ratings
    fields = ('Source', 'Value')


class FilmSerializer(serializers.ModelSerializer):
  Ratings = RatingsSerializer(many=True)

  class Meta:
    model = Film
    fields = ('id', 'Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre', 'Director', 'Writer', 'Actors', 'Plot',
              'Language', 'Country', 'Awards', 'Poster', 'Metascore', 'imdbRating', 'imdbVotes',
              'imdbID', 'Type', 'DVD', 'BoxOffice', 'Production', 'Website', 'Ratings')

  def create(self, validated_data):
    ratings_validated_data = validated_data.pop('Ratings')
    data_imdbVotes = validated_data.pop('imdbVotes')
    validated_data['imdbVotes'] = data_imdbVotes.replace(',', '')
    film = Film.objects.create(**validated_data)
    for rating in ratings_validated_data:
      Ratings.objects.create(film=film, **rating)
    return film


class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'

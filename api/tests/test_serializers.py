from rest_framework import serializers
from django.test import TestCase
from ..models import Ratings, Comment, Movie
from ..serializers import RatingsSerializer


class TestRatingsSerializer(TestCase):
  def setUp(self):
    
    self.rating_attributes = {
      'Source': 'Rotten Tomatoes',
      'Value': 9.7
    }
    
    self.serializer_data = {
      'Source': 'Rotten Tomatoes',
      'Value': 9.7
    }
    
    self.rating = Ratings.objects.create(**self.rating_attributes)
    self.serializer = RatingsSerializer(instance=self.rating)
  
  def test_contains_expected_fields(self):
    data = self.serializer.data
    
    self.assertEqual(set(data.keys()), set(['Source', 'Value']))

  def test_Source_field_content(self):
    data = self.serializer.data
  
    self.assertEqual(data['Source'], self.rating_attributes['Source'])

  def test_Value_field_content(self):
    data = self.serializer.data
  
    self.assertEqual(float(data['Value']), self.rating_attributes['Value'])


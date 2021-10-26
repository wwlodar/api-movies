from rest_framework.renderers import BrowsableAPIRenderer
from django import forms


class SomeApiForm(forms.Form):
  Title = forms.CharField(max_length=17, help_text='Please provide a valid movie title.')


class CustomBrowsableAPIRenderer(BrowsableAPIRenderer):
  OPTIONS_METHOD = "OPTIONS"
  
  def get_context(self, *args, **kwargs):
    context = super(CustomBrowsableAPIRenderer, self).get_context(*args, **kwargs)
    context['display_edit_forms'] = True
    form = SomeApiForm()
    context['post_form'] = form
    return context


from django.forms import ModelForm
from .models import Review, Tip
from django import forms


class ReviewForm(ModelForm):
  class Meta:
    model = Review
    fields = ['rating', 'title', 'content']
    widgets = {
      'content': forms.Textarea(attrs={'rows': 10, 'class': 'materialize-textarea'}),
    }

class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['title', 'content']
        widgets = {
          'content': forms.Textarea(attrs={'rows': 10, 'class': 'materialize-textarea'}),
        }
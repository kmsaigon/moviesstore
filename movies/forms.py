from django import forms
from .models import MovieRequest


class MovieRequestForm(forms.ModelForm):
    class Meta:
        model = MovieRequest
        fields = ['name', 'description']

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        normalized = ' '.join(name.split()).lower()
        return normalized


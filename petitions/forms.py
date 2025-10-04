from django import forms
from .models import Petition

class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['movie_title', 'description', 'genre', 'why_add_movie']
        widgets = {
            'movie_title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'why_add_movie': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean_movie_title(self):
        title = self.cleaned_data.get('movie_title', '')
        # Normalize the title (remove extra spaces, convert to title case)
        normalized = ' '.join(title.split()).title()
        return normalized

    def clean_genre(self):
        genre = self.cleaned_data.get('genre', '')
        # Normalize the genre (remove extra spaces, convert to title case)
        normalized = ' '.join(genre.split()).title()
        return normalized

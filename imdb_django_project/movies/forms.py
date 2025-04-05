from django import forms
from django.core.exceptions import ValidationError

class ReviewForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label='Content')
    rating = forms.IntegerField(label='Rating', min_value=1, max_value=10)

class MovieForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(widget=forms.Textarea, label='Description', required=False)
    release_year = forms.IntegerField(label='Release Year')
    genre = forms.CharField(label='Genre', max_length=100, required=False)

    def clean_release_year(self):
        release_year = self.cleaned_data['release_year']
        if release_year < 1888 or release_year > 2100:
            raise ValidationError("Release year must be between 1888 and 2100")
        return release_year
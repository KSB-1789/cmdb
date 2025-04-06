from django import forms
from django.core.exceptions import ValidationError
from .models import Movie, Review

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'year', 'genre', 'rating', 'poster']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min': '1888', 'max': '2100'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10', 'step': '0.1'}),
            'poster': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_year(self):
        year = self.cleaned_data['year']
        if year < 1888 or year > 2100:
            raise ValidationError("Year must be between 1888 and 2100")
        return year

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10',
                'step': '0.1',
                'required': True
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'required': True
            }),
        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 10:
            raise ValidationError("Rating must be between 1 and 10")
        return rating

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
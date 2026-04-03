from django import forms
from classes.models import StudioClass, Review


class CreateClassForm(forms.ModelForm):
    class Meta:
        model = StudioClass
        fields = [
            'title',
             'category',
             'instructor',
                'date',
                'duration',
                'capacity',
                'price',
                'image',
                'description',
                'is_published'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
                  'rating', 
                  'comment', 
                 ]
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

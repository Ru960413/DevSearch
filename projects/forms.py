from dataclasses import field
from django.forms import ModelForm
from .models import Project, Review
from django import forms

# create form based around model Project, and generate input fields
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'feature_image', 'description', 'demo_link', 'source_link']

        # change the tag field into checkboxes which user can select multiple of them at once
        widgets = {'tags': forms.CheckboxSelectMultiple(), }

    def __init__(self, *args, **kwargs):
        # go into the class ProjectForm and overwrite its init
        super(ProjectForm, self).__init__(*args, **kwargs)

        # take its title field and access its attribute(which is class here), and change it into input
        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder':'Add title'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})



class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

            
            
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
    
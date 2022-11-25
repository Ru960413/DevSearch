from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        
        # set the first_name field's label to Name
        labels = {
            'first_name': 'Name',
        }
    

    def __init__(self, *args, **kwargs):
        # go into the class CustomUserCreationForm and overwrite its init
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # take its title field and access its attribute(which is class here), and change it into input
        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder':'Add title'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username',
                  'location', 'bio', 'short_intro', 'profile_image',
                  'social_github', 'social_linkedin', 'social_twitter',
                  'social_youtube', 'social_website']
        
    def __init__(self, *args, **kwargs):
        # go into the class ProfileForm and overwrite its init
        super(ProfileForm, self).__init__(*args, **kwargs)

        # take its title field and access its attribute(which is class here), and change it into input
        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder':'Add title'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'

        # excluding the owner field from skill form
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

            

class MessageForm(ModelForm):
    class Meta:
         model = Message
         fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

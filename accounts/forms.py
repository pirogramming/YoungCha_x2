from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from .models import User, Profile


class SignupForm(UserCreationForm):
    name= forms.CharField(max_length=30,required=False)#꼭 필요는 아님
    score = forms.CharField(max_length=600,required=False)

    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         self.fields['username'].validators = [validate_email]
         self.fields['username'].help_text = 'Enter Email Format.'
         self.fields['username'].label = 'Email'


    def save(self):
        user = super().save(commit=False)
        user.email = user.username
        user.save()

        name = self.cleaned_data.get('name', None)
        score = self.cleaned_data.get('score', None)

        Profile.objects.create(user=user, name=name, score=score,)

        return user

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('name','score')


    '''
    def clean_username(self):
        value = self.cleaned_data.get('username')
        if value:
            valusr_idate_email(value)
        return value
    '''


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','score']


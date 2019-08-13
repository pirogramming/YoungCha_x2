from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from .models import User, Profile


class SignupForm(UserCreationForm):
    usr_id= forms.CharField(required=False)#꼭 필요는 아님
   # address = forms.URLField(required=False)

    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         self.fields['username'].validators = [validate_email]
         self.fields['username'].help_text = 'Enter Email Format.'
         self.fields['username'].label = 'Email'






    def save(self):
        user = super().save(commit=False)
        user.email = user.username
        user.save()
        usr_id = self.cleaned_data.get('usr_id', None)
        #address = self.cleaned_data.get('address', None)

        Profile.objects.create(user=user, usr_id=usr_id,)

        return user

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('usr_id',)


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
        fields = ['usr_id',]


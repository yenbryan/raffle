from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django import forms
from registration.models import Profile


class ProfileUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                          'placeholder': 'your email *'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'your username *'}))
    password1 = forms.CharField(label=("password"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'password *'}))
    password2 = forms.CharField(label=("Password"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                    'placeholder': 're-enter password *'}))

    class Meta:
        model = Profile
        fields = ("email", "username", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'your username *'}))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'password *'}))


class ResetPWord(PasswordResetForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                          'placeholder': 'your email *'}))


class PictureForm(forms.Form):
    picture = forms.ImageField()
    description = forms.CharField(max_length=125, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                'placeholder': 'description'}))


class AboutMeForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                                'placeholder': 'description'}))


class ProfileForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'first name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'last name'}))

class AccountForm(forms.Form):
    pass
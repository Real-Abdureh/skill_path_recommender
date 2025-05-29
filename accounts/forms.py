from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile

class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form with styled form controls"""
    
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'autofocus': True
            }
        )
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )
    )

class SignUpForm(UserCreationForm):
    """Form for user registration with additional profile fields"""
    
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }
        )
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }
        )
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }
        )
    )
    
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }
        )
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password'
            }
        )
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information"""
    
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Tell us a bit about yourself',
                'rows': 3
            }
        )
    )
    
    current_position = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Current Job Title'
            }
        )
    )
    
    experience_level = forms.ChoiceField(
        choices=UserProfile.EXPERIENCE_LEVELS,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )
    
    learning_goal = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'What do you want to achieve?'
            }
        )
    )
    
    class Meta:
        model = UserProfile
        fields = ('bio', 'current_position', 'experience_level', 'learning_goal')

class UserUpdateForm(forms.ModelForm):
    """Form for updating user information"""
    
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class UserUpdateForm(UserChangeForm):
    # Set password to None to remove it from the form.
    # Password changes should be handled by a separate dedicated form.
    password = None

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        # Exclude 'password' as we are not handling password changes here.
        # widgets = {
        #     'password': forms.PasswordInput(render_value=False), # Not needed if password = None
        # }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        # The UserChangeForm includes the password field by default, which we don't want.
        # We've set it to None above, but to be sure it's not part of the form fields:
        if 'password' in self.fields:
            del self.fields['password']

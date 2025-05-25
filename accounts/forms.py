from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

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

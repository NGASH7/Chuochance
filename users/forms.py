from django.shortcuts import redirect
from django import forms
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group

from bootstrap_modal_forms.forms import BSModalModelForm
from allauth.account.forms import LoginForm, SignupForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, HTML
from crispy_forms.bootstrap import AppendedText, PrependedText


User = get_user_model()
''' LOGIN FORM '''


class LoginForm(LoginForm):
    """docstring for LoginForm"""

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields["login"].label = ""
        self.fields["password"].label = ""
        self.helper.layout = Layout(
            Field('login', placeholder="Email Address or ID Number"),
            AppendedText('password', '<i class="fas fa-eye-slash" id="eye" onclick="showHidePwd();"></i>',
                         placeholder="Enter Password"),

            Field('remember'),
        )


''' EMPLOYEES REGISTRATION FORM '''


class RegistrationForm(UserCreationForm):
    # gender = forms.ChoiceField(choices=GENDER, required=False)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name',
            'id_number', 'email',
            'password1', 'password2'
        ]

    def signup(self, request, user):
        login(request, user)

        messages.success(request, 'Account Created Successfully')
        return redirect('home')

    def save(self, commit=False):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = user.id_number
        user.user_type = 2
        user.save()
        user.refresh_from_db()

        return user

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.fields['id_number'].required = True
        self.fields['email'].required = True

        self.fields['id_number'].label = 'ID Number'
        self.fields['password1'].label = 'Create Password'
        self.fields['password2'].label = 'Verify Password'

        self.fields['password1'].help_text = 'Ensure your password has atleast 8 characters and one number'

        self.helper.layout = Layout(
            Row(
                Column(
                    Field('first_name', css_id="",
                          css_class="", label='First Name'),
                ),
                Column(
                    Field('last_name', css_id="",
                          css_class="", label='Last Name'),
                ),
            ),
            HTML('<hr/>'),
            Row(
                Column(
                    Field('id_number', css_id="",
                          css_class="", label='ID Number'),
                ),
                Column(
                    Field('email', css_id="", css_class=""),
                ),
            ),
            HTML('<hr/>'),
            Row(
                Column(
                    AppendedText(
                        'password1', '<i class="fas fa-eye-slash" id="eye" onclick="showHidePwd();"></i>'),
                ),
                Column(
                    AppendedText(
                        'password2', '<i class="fas fa-eye-slash" id="eye2" onclick="showHidePwd();"></i>'),
                )
            ),
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'other_names',
                  'date_of_birth', 'gender', 'phone']

    """docstring for ProfileForm"""

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column(
                    Field('first_name', css_id="", css_class=""),
                ),
                Column(
                    Field('last_name', css_id="", css_class=""),
                ),
                Column(
                    Field('other_names', css_id="", css_class=""),
                ),
            ),
            Row(
                Column(
                    Field('date_of_birth', css_id="", css_class=""),
                ),
                Column(
                    Field('gender', css_id="", css_class=""),
                ),
            ),
            Row(
                Column(
                    Field('phone', css_id="", css_class="phone_input"),
                )
            ),
        )

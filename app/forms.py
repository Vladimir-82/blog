from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Post



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'style': 'width:50ch'
                                      })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'style': 'width:50ch'
                                          })
                                )


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Name',
                               help_text='Maximum 150 characters',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'style': 'width:50ch'
                                          })
                               )
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                           'style': 'width:50ch'
                                           })
                                )
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                           'style': 'width:50ch'
                                           })
                                )
    email = forms.EmailField(label='E-mail',
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control',
                                        'style': 'width:50ch'})
                             )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

from .models import Post, Comment, Category


class ContactForm(forms.Form):
    subject = forms.CharField(
        label='subject',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'style': 'width:50ch'
                                      }))
    content = forms.CharField(
        label='content',
        widget=forms.Textarea(attrs={'class': 'form-control',
                                     'style': 'width:50ch',
                                     'rows': 5
                                      }))
    captcha = CaptchaField()


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


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'photo', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'style': 'width:50ch'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5,
                                          'style': 'width:50ch'}),
            'category': forms.Select(attrs={'class': 'form-control',
                                            'style': 'width:50ch'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {
            'body': 'Your comment:',
        }
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control',
                                                  'rows': 5,
                                                  'style': 'width:50ch',
                                          }
                                   ),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'style': 'width:50ch'}),
        }



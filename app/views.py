from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import UserRegisterForm, UserLoginForm
from .utils import *



from django.views.generic.list import ListView
from .models import Post, Category


class MainListView(ListView):
    template_name = 'main.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['post'] = Post.objects.all()
        return context

class CategoryListView(ListView):
    template_name = 'main.html'
    context_object_name = 'post'


    def get_queryset(self):
        return Post.objects.filter(
            category_id=self.kwargs['category_id']).select_related('category')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['post'] = Post.objects.filter(
            category_id=self.kwargs['category_id']).select_related('category')
        return context





def register(request):
    '''
    Registration of service users
    '''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, Message.success_register)
            return redirect('/')
        else:
            messages.error(request, Message.error_register)
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {"form": form})


def user_login(request):
    '''
    Service user logging
    '''
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {"form": form})


def user_logout(request):
    '''
    Unlogging service users
    '''
    logout(request)
    return redirect('login')

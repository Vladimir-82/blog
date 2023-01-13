from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, \
    UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from .forms import UserRegisterForm, UserLoginForm, PostForm, CommentForm
from .utils import *



from .models import Post, Category, Comment


class MainListView(ListView):
    template_name = 'main.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        context['post'] = Post.objects.filter(
            category_id=self.kwargs['category_id']).select_related('category')
        return context


class CreatePost(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'create.html'
    success_url = reverse_lazy('main')
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)




class UpdateComment(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'update_comment.html'
    # queryset = Post

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if obj.name != self.request.user:
            raise PermissionDenied()
        return obj

    def get_success_url(self):
        pk = self.kwargs["pk"]
        current_post = Post.objects.get(comment__id=pk)
        return reverse('view_news', kwargs={"pk": current_post.pk})



class UpdatePost(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'update.html'

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if obj.author != self.request.user:
            raise PermissionDenied()
        return obj

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse('view_news', kwargs={"pk": pk})


class DeletePost(DeleteView):
    model = Post
    success_url = reverse_lazy('main')
    template_name = 'delete.html'


    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if obj.author != self.request.user:
            raise PermissionDenied()
        return obj


class ViewPost(FormMixin, DetailView):
    form_class = CommentForm
    model = Post
    context_object_name = 'post_item'
    template_name = 'post_detail.html'


    def get_object(self):
        '''
        Increases the number of views
        '''
        object = super().get_object()
        object.views += 1
        object.save()
        return object


    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse('view_news', kwargs={"pk": pk})


    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        queryset = Comment.objects.filter(post=self.object)
        context['comments'] = queryset
        context['count_comments'] = queryset.count()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        self.object = self.get_object()
        name = request.user
        comment = request.POST['body']
        Comment.objects.create(post=self.object, name=name,
                               email=name.email, body=comment
                               )
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)




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

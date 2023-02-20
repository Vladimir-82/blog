from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, \
    UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.db.models import Q
from .forms import UserRegisterForm, UserLoginForm, PostForm, CommentForm
from .utils import *
from .models import Post, Comment, Profile
import json


class MainListView(ListView):
    """Shows all posts on the main page"""
    template_name = 'main.html'
    context_object_name = 'post'
    model = Post


class CategoryListView(ListView):
    """Shows posts by category on the main page"""
    template_name = 'main.html'

    def get_queryset(self):
        """Returns posts by category"""
        return Post.objects.filter(
            category_id=self.kwargs['category_id']).select_related('category')

    def get_context_data(self, **kwargs):
        """Returns contexts name"""
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.filter(
            category_id=self.kwargs['category_id']).select_related('category')
        return context


class CreatePost(LoginRequiredMixin, CreateView):
    """Create new post"""
    form_class = PostForm
    template_name = 'create.html'
    success_url = reverse_lazy('main')
    login_url = '/login/'

    def form_valid(self, form):
        """Form validation"""
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateComment(UpdateView):
    """Update comment"""
    model = Comment
    form_class = CommentForm
    template_name = 'update_comment.html'

    def get_object(self, *args, **kwargs):
        """Comment author validation"""
        obj = super().get_object(*args, **kwargs)
        if obj.name != self.request.user:
            raise PermissionDenied()
        return obj

    def get_success_url(self):
        """Redirect to current post"""
        pk = self.kwargs["pk"]
        current_post = Post.objects.get(comment__id=pk)
        return reverse('view_news', kwargs={"pk": current_post.pk})


class UpdatePost(UpdateView):
    """Update post"""
    model = Post
    form_class = PostForm
    template_name = 'update.html'

    def get_object(self, *args, **kwargs):
        """Post author validation"""
        obj = super().get_object(*args, **kwargs)
        if obj.author != self.request.user:
            raise PermissionDenied()
        return obj

    def get_success_url(self):
        """Redirect to current post"""
        pk = self.kwargs["pk"]
        return reverse('view_news', kwargs={"pk": pk})


class DeletePost(DeleteView):
    """Delete post"""
    model = Post
    success_url = reverse_lazy('main')
    template_name = 'delete.html'

    def get_object(self, *args, **kwargs):
        """Post author validation"""
        obj = super().get_object(*args, **kwargs)
        if obj.author != self.request.user:
            raise PermissionDenied()
        return obj


class ViewPost(FormMixin, DetailView):
    """Detail view post"""
    form_class = CommentForm
    model = Post
    context_object_name = 'post_item'
    template_name = 'post_detail.html'

    def get_success_url(self):
        """Redirect to current post"""
        pk = self.kwargs["pk"]
        return reverse('view_news', kwargs={"pk": pk})

    def get_context_data(self, **kwargs):
        """Increases the number of views, shows comments, flags of likes"""
        object = super().get_object()
        object.views += 1
        object.save()
        msg = False
        current_user_id = self.request.user.id
        if object.likes.filter(id=current_user_id).exists():
            msg = True

        context = super().get_context_data(**kwargs)
        queryset = Comment.objects.filter(post=object)
        context['comments'] = queryset
        context['count_comments'] = queryset.count()
        context['msg'] = msg
        return context

    def post(self, request, *args, **kwargs):
        """Create new post"""
        if not request.user.is_authenticated:
            raise PermissionDenied()
        obj = self.get_object()
        name = request.user
        comment = request.POST['body']
        Comment.objects.create(post=obj, name=name,
                               email=name.email, body=comment
                               )
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def register(request):
    """Registration of service users"""
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
    """Service user logging"""
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
    """Unlogging service users"""
    logout(request)
    return redirect('login')


def like_post(request):
    """likes manager"""
    data = json.loads(request.body)
    current_post_id = data["id"]
    post = Post.objects.get(id=current_post_id)
    cheker = None

    if request.user.is_authenticated:
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            cheker = 0
        else:
            post.likes.add(request.user)
            cheker = 1

    likes = post.likes.count()

    info = {
        "check": cheker,
        "number_of_likes": likes,
    }

    return JsonResponse(info, safe=False)


class SearchResultsView(ListView):
    """Search in posts by title and content"""
    model = Post
    template_name = "search.html"
    context_object_name = 'search'

    def get_queryset(self):
        """search in posts by title and content"""
        query = self.request.GET.get('search')
        if query:
            result = Post.objects.filter(Q(
                title__icontains=query) | Q(
                body__icontains=query))
        else:
            result = None
        return result


def author_info(request, author_id):
    """return following users"""
    current_user = request.user.id
    author = User.objects.get(id=author_id)

    current_users_friends_list = get_current_following(request=request)

    all_user_friends = \
        Profile.objects.prefetch_related('friends').all()
    all_user_friend_list = \
        [user.name.username for user in all_user_friends]

    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('_method') == 'add':
                if author.username not in current_users_friends_list:

                    if author.username not in all_user_friend_list:
                        new_friend = Profile.objects.create(name=author)
                    else:
                        new_friend = Profile.objects.get(name=author)
                    new_friend.friends.add(current_user)
            else:
                ex_friend = Profile.objects.get(name=author)
                ex_friend.friends.remove(current_user)

    current_users_friends_list = get_current_following(request=request)
    is_friend = author.username in current_users_friends_list

    return render(request, 'author.html', {"author_info": author,
                                            "is_friend": is_friend,
                                           })


def get_current_following(request) -> list:
    """return current users friends list"""
    current_user = request.user.id
    current_users_friends = Profile.objects.filter(friends=current_user)
    current_users_friends_list = \
        [user.name.username for user in current_users_friends]
    return current_users_friends_list


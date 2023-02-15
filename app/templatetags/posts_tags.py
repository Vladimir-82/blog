from django import template
from django.db.models import Count
from django.contrib.auth.models import User

from app.models import Category, Profile, Post


register = template.Library()


@register.inclusion_tag('list_categories.html')
def show_categories():
    categories = Category.objects.annotate(cnt=Count('post'))
    return {'categories': categories}


@register.inclusion_tag('list_following.html', takes_context=True)
def show_following(context):
    request = context['request']
    current_user = request.user.id
    following = Profile.objects.filter(friends=current_user)
    return {'following': following}


@register.inclusion_tag('list_followers.html', takes_context=True)
def show_followers(context, author_id):
    request = context['request']

    if request.user.is_authenticated:



        followers = Profile.objects.filter(name=author_id)
        return {'followers': followers}
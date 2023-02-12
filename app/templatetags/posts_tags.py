from django import template
from django.db.models import Count

from app.models import Category, Profile


register = template.Library()


@register.inclusion_tag('list_categories.html')
def show_categories():
    categories = Category.objects.annotate(cnt=Count('post'))
    return {'categories': categories}


@register.inclusion_tag('list_followings.html', takes_context=True)
def show_followings(context):
    request = context['request']
    current_user = request.user.id
    followings = Profile.objects.filter(friends=current_user)
    return {'followings': followings}
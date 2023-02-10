from django import template
from django.db.models import Count

from app.models import Category, Profile


register = template.Library()


@register.inclusion_tag('list_categories.html')
def show_categories():
    categories = Category.objects.annotate(cnt=Count('post'))
    return {'categories': categories}


@register.inclusion_tag('list_followings.html')
def show_followings():
    followings = Profile.objects.prefetch_related('friends').all()
    return {'followings': followings}
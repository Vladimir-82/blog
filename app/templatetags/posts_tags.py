from django import template
from django.db.models import Count



from app.models import Category, Profile

from app.views import get_followings

register = template.Library()


@register.inclusion_tag('list_categories.html')
def show_categories():
    categories = Category.objects.annotate(cnt=Count('post'))
    return {'categories': categories}


@register.inclusion_tag('list_followings.html')
def show_followings():
    followings = get_followings()
    return {'followings': followings}
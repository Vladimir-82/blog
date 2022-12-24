from django import template

from app.models import Category

register = template.Library()


@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('basic.html')
def show_categories():
    categories = Category.objects.all()
    return {"categories": categories}

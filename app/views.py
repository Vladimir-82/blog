from django.views.generic.list import ListView
from .models import Post, Category


class MainListView(ListView):
    template_name = 'main.html'
    model = Category

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

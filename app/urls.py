from django.urls import path
from .views import *


urlpatterns = [
    path('', MainListView.as_view(), name='main'),
    path('create', CreatePost.as_view(), name='create'),
    path('category/<int:category_id>/',
         CategoryListView.as_view(), name='category'),
    path('post/<int:pk>/', ViewPost.as_view(), name='view_news'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
            ]
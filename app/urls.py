from django.urls import path
from .views import *


urlpatterns = [
    path('', MainListView.as_view(), name='main'),
    path('create', CreatePost.as_view(), name='create'),
    path('comment/<int:pk>/update_comment', UpdateComment.as_view(), name='update_comment'),
    path('post/<int:pk>/update', UpdatePost.as_view(), name='update'),
    path('post/<int:pk>/delete', DeletePost.as_view(), name='delete'),
    path('category/<int:category_id>/',
         CategoryListView.as_view(), name='category'),
    path('post/<int:pk>/', ViewPost.as_view(), name='view_news'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('like_post', like_post, name='like'),
            ]
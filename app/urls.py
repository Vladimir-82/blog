from django.urls import path
from .views import *


urlpatterns = [
    path('', MainListView.as_view(), name='main'),
    path('create', CreatePost.as_view(), name='create'),
    path('create_category', CreateCategory.as_view(), name='create_category'),
    path('comment/<int:pk>/update_comment', UpdateComment.as_view(), name='update_comment'),
    path('post/<int:pk>/update', UpdatePost.as_view(), name='update'),
    path('post/<int:pk>/delete', DeletePost.as_view(), name='delete'),
    path('category/<int:category_id>/',
         CategoryListView.as_view(), name='category'),
    path('post/<int:pk>/', ViewPost.as_view(), name='view_news'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('send/', mail_send, name='send'),
    path('like_post', like_post, name='like'),
    path('search', SearchResultsView.as_view(), name='search'),
    path('author/<int:author_id>/', author_info, name='author'),
            ]
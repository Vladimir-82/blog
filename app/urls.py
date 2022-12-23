from django.urls import path
from .views import MainListView, CategoryListView, register, user_login, \
    user_logout


urlpatterns = [
    path('', MainListView.as_view(), name='main'),
    path('<int:category>', CategoryListView(), name='category'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
            ]
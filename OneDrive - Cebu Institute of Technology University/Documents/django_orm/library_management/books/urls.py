from django.urls import path
from . import views

urlpatters = [
    path('', views.book_list, name='book_list'),
]
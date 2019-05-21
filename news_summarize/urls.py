from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.news_home, name='news_home'),
    path("news_summarize/", views.summarize, name='news_summary'),
    path("search_stock/", views.search_stock, name='search_stock'),
]

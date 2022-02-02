from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    #path('', cache_page(60*1)(NewsList.as_view()) , name="news_list"),
    path('', NewsList.as_view() , name="news_list"),
    path('<int:pk>', NewsDetailView.as_view(), name="news_detail"),
    path('category/<int:pk>/', cache_page(60*5)(CategoryView.as_view()), name="category_detail"),
    path('category/<int:pk>/subscribe/', SubscribeView.as_view(), name="category_subscribe"),
    path('search/', SearchListView.as_view(), name="search"),
    path('add/', NewsCreateView.as_view(), name="news_add"),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
]
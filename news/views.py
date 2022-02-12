from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .filters import SearchFilter 
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from datetime import datetime
from django.core.cache import cache
from django.http.response import HttpResponse #  импортируем респонс для проверки текста
from .models import *
from django.utils import timezone
from django.utils.translation import activate, get_supported_language_variant, LANGUAGE_SESSION_KEY
from django.utils.translation import gettext as _ #  импортируем функцию для перевода
import pytz #  импортируем стандартный модуль для работы с часовыми поясами

from rest_framework import viewsets
from rest_framework import permissions

from .serializers import *


class NewsList(ListView):
    model = Post  
    template_name = 'news_list.html' 
    context_object_name = 'news_list'
    ordering = ['-date']
    paginate_by = 10
    queryset = Post.objects.order_by('-date') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class NewsCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news_edit.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

class NewsDetailView(DetailView):
    model = Post  
    template_name = 'news_detail.html' 
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context
        
class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'news_edit.html'
    form_class = PostForm
    permission_required = ('news.change_post', )
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context  

class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    context_object_name = 'news'
    permission_required = ('news.delete_post', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

class SearchListView(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = SearchFilter(self.request.GET, queryset=self.get_queryset())
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context
        
    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class CategoryView(DetailView):
    model = Category  
    template_name = 'category_detail.html' 
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

class SubscribeView(View):
    def get(self, request, *args, **kwargs):
        category=Category.objects.get(pk=kwargs['pk'])
        user = request.user
        category.subscribers.add(user)
    
        return redirect('category_detail',category.pk)
    # отправляем письмо
    # send_mail( 
    #     subject=f'Новый подписчик',
    #     message=f'Пользователь {user.username} подписался на категорию {category}', 
    #     from_email=None,
    #     recipient_list=[user.email]
    # )  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context
        
    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

class NewsViewset(viewsets.ModelViewSet):
   queryset = Post.objects.all().filter(type = "Н")
   serializer_class = PostSerializer
   permission_classes = [permissions.IsAuthenticated]

class ArticlesViewset(viewsets.ModelViewSet):
   queryset = Post.objects.all().filter(type = "С")
   serializer_class = PostSerializer
   permission_classes = [permissions.IsAuthenticated] 
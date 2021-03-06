from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from datetime import datetime, timedelta

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context
    
# class Index(View):
#     def get(self, request):
#         printer.apply_async([10], eta = datetime.now() + timedelta(seconds=5))
#         hello.delay()
#         return HttpResponse('Hello!')
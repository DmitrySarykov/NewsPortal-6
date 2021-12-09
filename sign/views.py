from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from news.models import Author

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

@login_required
def upgrade_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    if not Author.objects.filter(user=user).exists():
        Author.objects.create(user=user)
    return redirect('/')
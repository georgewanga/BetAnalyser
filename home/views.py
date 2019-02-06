from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic.list import ListView
from home.models import Home
from home.update import update_games

def add_games(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    av_list = Home.objects.all().values_list('match_date')
    update_games(av_list)
    if is_safe_url(redirect_path, request.get_host()):
        return redirect(redirect_path)
    return redirect('home_page:index')


def delete_all(request):
    Home.objects.all().delete()
    return redirect('home_page:index')


class HomeListView(ListView):
    template_name = 'home/index.html'

    def get_queryset(self,*args,**kwargs):
        return Home.objects.all()

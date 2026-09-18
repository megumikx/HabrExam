from django.shortcuts import render
from .models import News
from .forms import NewsForm

def news(request):
    news_list = News.objects.order_by('-data')
    return render(request, 'news/news_home.html', {'news': news})

def create(request):
    form = NewsForm()
    data = {'form': form}
    return render(request, 'news/create.html', data)
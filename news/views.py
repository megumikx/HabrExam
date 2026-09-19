from calendar import error

from django.shortcuts import render, redirect
from .models import News
from .forms import NewsForm
from django.views.generic import DetailView

def news(request):
    news_list = News.objects.order_by('-data')
    return render(request, 'news/news_home.html', {'news': news_list})

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/details_view.html'
    context_object_name = 'post'
def create(request):
    error = ''
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news')
        else:
            error = 'Форма была неверной'
    form = NewsForm()
    data = {'form': form,
            'error': error
    }

    return render(request, 'news/create.html', data)
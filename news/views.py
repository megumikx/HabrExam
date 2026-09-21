from django.shortcuts import render, redirect
from .models import News
from .forms import NewsForm
from django.views.generic import DetailView, UpdateView, DeleteView


def news(request):
    news_list = News.objects.order_by('-data')
    return render(request, 'news/news_home.html', {'news': news_list})


class NewsUpdateView(UpdateView):
    model = News
    template_name = 'news/create.html'
    form_class = NewsForm


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/details_view.html'
    context_object_name = 'post'


class NewsDeleteView(DeleteView):
    model = News
    template_name = 'news/news-delete.html'
    success_url = '/news/'


def create(request):
    error = ''

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('news')

        error = 'Форма была неверной'

    else:
        form = NewsForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'news/create.html', data)
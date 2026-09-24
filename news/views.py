from django.shortcuts import render, redirect, get_object_or_404
from .models import News, Category, Bookmark, Rating
from .forms import NewsForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group, User
from django.contrib.auth.models import User

def categories(request):
    categories_list = Category.objects.all()
    return render(request, "news/categories.html", {"categories": categories_list})


def category_news(request, pk):
    category = Category.objects.get(pk=pk)
    news_list = News.objects.filter(category=category).order_by("-data")

    return render(
        request, "news/category_news.html", {"category": category, "news": news_list}
    )


def news(request):
    news_list = News.objects.filter(
        status="approved"
    ).annotate(
        avg_rating=Avg('ratings__value')
    ).order_by('-data')

    rating_filter = request.GET.get("rating")

    if rating_filter:
        try:
            rating_filter = int(rating_filter)

            if 1 <= rating_filter <= 5:
                news_list = news_list.filter(avg_rating__gte=rating_filter)
        except ValueError:
            pass

    return render(
        request,
        "news/news_home.html",
        {"news": news_list, "rating_filter": rating_filter},
    )


class NewsUpdateView(UpdateView):
    model = News
    template_name = "news/create.html"
    form_class = NewsForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied

        self.object = self.get_object()

        is_admin = (
            request.user.is_superuser
            or request.user.groups.filter(name="Admin").exists()
        )

        is_author = self.object.author == request.user

        if not (is_admin or is_author):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class NewsDetailView(DetailView):
    model = News
    template_name = "news/details_view.html"
    context_object_name = "post"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        is_admin = (
            request.user.is_superuser
            or request.user.groups.filter(name="Admin").exists()
        )

        is_author = (
            request.user.is_authenticated
            and self.object.author == request.user
        )

        if self.object.status != "approved" and not (is_admin or is_author):
            raise PermissionDenied


        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.object

        ratings = post.ratings.all()

        context["rating_count"] = ratings.count()

        if ratings.exists():
            context["average_rating"] = round(
                sum(rating.value for rating in ratings) / ratings.count(), 1
            )
        else:
            context["average_rating"] = 0

        if self.request.user.is_authenticated:
            user_rating = ratings.filter(user=self.request.user).first()

            context["user_rating"] = user_rating.value if user_rating else None
        else:
            context["user_rating"] = None

        return context


class NewsDeleteView(DeleteView):
    model = News
    template_name = "news/news-delete.html"
    success_url = "/news/"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied

        self.object = self.get_object()

        is_admin = (
            request.user.is_superuser
            or request.user.groups.filter(name="Admin").exists()
        )

        is_author = self.object.author == request.user

        if not (is_admin or is_author):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


@login_required
def toggle_bookmark(request, pk):
    news = get_object_or_404(News, pk=pk)

    bookmark = Bookmark.objects.filter(user=request.user, news=news).first()

    if bookmark:
        bookmark.delete()
    else:
        Bookmark.objects.create(user=request.user, news=news)

    return redirect("detail", pk=pk)


@login_required
def favorites(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related(
        "news", "news__category", "news__author"
    )

    return render(request, "news/favorites.html", {"bookmarks": bookmarks})


@login_required
def rate_news(request, pk):
    news = get_object_or_404(News, pk=pk)

    if request.method == "POST":
        value = int(request.POST.get("rating", 0))

        if 1 <= value <= 5:
            Rating.objects.update_or_create(
                user=request.user, news=news, defaults={"value": value}
            )

    return redirect("detail", pk=pk)


@login_required
def create(request):
    error = ""

    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)

        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.status = "pending"
            news.save()
            return redirect('news')

        error = "Форма была неверной"

    else:
        form = NewsForm()

    data = {"form": form, "error": error}

    return render(request, "news/create.html", data)


@login_required
def moderation(request):
    is_admin = (
        request.user.is_superuser
        or request.user.groups.filter(name="Admin").exists()
    )

    if not is_admin:
        raise PermissionDenied

    news_list = News.objects.filter(
        status="pending"
    ).order_by("-data")

    return render(
        request,
        "news/moderation.html",
        {"news": news_list}
    )

@login_required
def approve_news(request, pk):
    is_admin = (
        request.user.is_superuser
        or request.user.groups.filter(name="Admin").exists()
    )

    if not is_admin:
        raise PermissionDenied

    news = get_object_or_404(News, pk=pk)

    if request.method == "POST":
        news.status = "approved"
        news.save()

    return redirect("moderation")

@login_required
def reject_news(request, pk):
    is_admin = (
        request.user.is_superuser
        or request.user.groups.filter(name="Admin").exists()
    )

    if not is_admin:
        raise PermissionDenied

    news = get_object_or_404(News, pk=pk)

    if request.method == "POST":
        news.status = "rejected"
        news.save()

    return redirect("moderation")

@login_required
def users_management(request):
    is_admin = (
        request.user.is_superuser
        or request.user.groups.filter(name="Admin").exists()
    )

    if not is_admin:
        raise PermissionDenied

    users = User.objects.all().order_by("username")

    for user_item in users:
        user_item.is_admin_group = user_item.groups.filter(
            name="Admin"
        ).exists()

    return render(
        request,
        "main/users_management.html",
        {"users": users},
    )

@login_required
def toggle_user_ban(request, pk):
    is_admin = (
        request.user.is_superuser
        or request.user.groups.filter(name="Admin").exists()
    )

    if not is_admin:
        raise PermissionDenied

    user = get_object_or_404(User, pk=pk)

    if user == request.user or user.is_superuser:
        return redirect("users-management")

    if request.method == "POST":
        user.is_active = not user.is_active
        user.save()

    return redirect("users-management")

@login_required
def toggle_admin(request, pk):
    if not request.user.is_superuser:
        raise PermissionDenied

    user = get_object_or_404(User, pk=pk)

    admin_group = Group.objects.get(name="Admin")

    if request.method == "POST":
        if admin_group in user.groups.all():
            user.groups.remove(admin_group)
        else:
            user.groups.add(admin_group)

    return redirect("users-management")

def authors(request):
    authors_list = User.objects.filter(
        news__status="approved"
    ).distinct().order_by("username")

    return render(
        request,
        "news/authors.html",
        {"authors": authors_list},
    )
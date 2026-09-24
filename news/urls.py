from django.urls import path
from . import views

urlpatterns = [
    path("", views.news, name="news"),
    path("create/", views.create, name="create"),
    path("<int:pk>/", views.NewsDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.NewsUpdateView.as_view(), name="news-update"),
    path("<int:pk>/delete/", views.NewsDeleteView.as_view(), name="news-delete"),
    path("categories/", views.categories, name="categories"),
    path("categories/<int:pk>/", views.category_news, name="category-news"),
    path("bookmark/<int:pk>/", views.toggle_bookmark, name="toggle-bookmark"),
    path("favorites/", views.favorites, name="favorites"),
    path("rate/<int:pk>/", views.rate_news, name="rate-news"),
    path('moderation/', views.moderation, name='moderation'),
    path('approve/<int:pk>/', views.approve_news, name='approve-news'),
    path('reject/<int:pk>/', views.reject_news, name='reject-news'),
    path("users/", views.users_management, name="users-management"),
    path("users/<int:pk>/ban/", views.toggle_user_ban, name="toggle-user-ban"),
    path("users/<int:pk>/admin/", views.toggle_admin, name="toggle-admin"),
    path('authors/', views.authors, name='authors'),
]

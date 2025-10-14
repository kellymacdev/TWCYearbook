
from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('admin', admin.site.urls),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/<str:profile_name>", views.all_posts, name="all_posts"),
    path("post/<int:post_id>", views.edit_post, name="edit_post"),
    path("<int:grad_id>", views.profile, name="profile"),
    path("summary", views.summary, name="summary"),
    path("memoriam/<str:person>", views.memoriam, name="memoriam"),
    path("<str:profile_name>/following", views.following, name="following"),
    path("toggle_follow/<str:profile_name>/", views.toggle_follow, name="toggle_follow"),
    path("toggle_like/<int:post_id>/", views.toggle_like, name="toggle_like"),
]

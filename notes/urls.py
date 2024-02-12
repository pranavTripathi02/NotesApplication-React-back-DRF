from django.urls import path

from . import views

urlpatterns = [
    path("notes", views.notes_list, name="index"),
    path("notes/<int:pk>", views.note_details, name="details"),
    path("auth/login", views.login_user, name="login"),
    path("auth/register", views.register_user, name="register"),
    path("auth/logout", views.logout_user, name="logout"),
]

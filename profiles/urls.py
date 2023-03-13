from django.urls import path

from profiles.views import LoginView, LogoutView

app_name = "profiles"
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

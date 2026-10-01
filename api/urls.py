from django.urls import path
from .views import LoginView, ProfileView

urlpatterns = [
    path("api/login/", LoginView.as_view()),
    path("api/profile/", ProfileView.as_view()),
]

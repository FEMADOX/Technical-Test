from django.urls import path

from account.views import LoginView, SignUpView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
]

from django.urls import path

from proxy.views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view()),
]

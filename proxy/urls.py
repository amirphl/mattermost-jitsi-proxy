from django.urls import path

from proxy.views import LoginView, MessageView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('rooms/<str:room_id>/messages/', MessageView.as_view()),
]

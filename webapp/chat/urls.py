from django.urls import path

from chat.views import ChatView

urlpatterns = [
    path("", ChatView.as_view()),
]

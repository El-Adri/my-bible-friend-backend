from django.urls import path

from .views import AdviceView, ChatView, StoryView

urlpatterns = [
    path("chat", ChatView.as_view(), name="chat"),
    path("advice", AdviceView.as_view(), name="advice"),
    path("story", StoryView.as_view(), name="story"),
]


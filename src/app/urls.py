from django.contrib import admin
from django.urls import path
from bot.views import slack_events

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bot/slack_event/', slack_events),
]

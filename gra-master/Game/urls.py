from django.urls import path
from Game.views import score_response

urlpatterns = [
    path('score/', score_response),
]
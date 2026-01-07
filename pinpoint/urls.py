from django.urls import path
from .views import PinDropView, MemoDropView, PinProximityView, MemoProximityView

urlpatterns = [
    path('points/', PinDropView.as_view()),
    path('points/messages/', MemoDropView.as_view()),
    path('points/search/', PinProximityView.as_view()),
    path('points/messages/search/', MemoProximityView.as_view()),
]